"""TITO's TRUEQUES option on the real map UI: the list of everyone the player can still trade with, and where."""
import io
import json
import re
import sys
from pathlib import Path

from pyboy import PyBoy
from cpu_harness import ROM, Routine, addr, symbols

results = []


def check(name, value=True):
    assert value, name
    results.append({"name": name, "passed": True})
    print("PASS", name, flush=True)


def offset(name):
    bank, pointer = symbols[name]
    return bank * 0x4000 + pointer - 0x4000 if bank else pointer


charmap = {}
for line in Path('work/source/constants/charmap.asm').read_text(encoding='utf8').splitlines():
    m = re.match(r'\s*charmap "(.+?)",\s*\$([0-9a-fA-F]{2})', line)
    if m and int(m[2], 16) not in charmap:
        charmap[int(m[2], 16)] = m[1]


def screen_rows(p):
    tiles = list(p.memory[addr('wTilemap'):addr('wTilemap') + 360])
    return [''.join(charmap.get(b, '?') if b != 0x7f else ' ' for b in tiles[y * 20:(y + 1) * 20]) for y in range(18)]


class Center:
    def __init__(self, full_moves=False):
        data = bytearray(ROM.read_bytes())
        for name in ["PlayerProfileSetup", "OakSpeech", "ShrinkPlayer", "_InitializeStartDay"]:
            data[offset(name)] = 0xC9
        start = offset("SpawnPoints")
        data[start:start + 4] = data[start + 4:start + 6] + bytes([6, 5])
        self.p = PyBoy(io.BytesIO(data), window="null", sound_emulated=False, log_level="ERROR")
        self.p.set_emulation_speed(0)
        self.counts = {}
        for name in ["TitoXeluisServices.WaitMainMenu", "SelectTradeOrDayCareMon", "TitoXeluisTrade",
                     "TitoMoveReminder", "ScrollingMenu", "LearnMove", "YesNoBox",
                     "TradeAnimation", "DoPreparedNPCTrade"]:
            def hook(_, name=name):
                self.counts[name] = self.counts.get(name, 0) + 1
            self.p.hook_register(*symbols[name], hook, None)
        self.p.tick(360)
        self.press("start", 120)
        self.press("start", 120)
        self.p.button_press("a")
        self.p.tick(32)
        self.p.button_release("a")
        self.p.tick(300)
        p = self.p
        p.memory[addr("wOptions")] = (p.memory[addr("wOptions")] & 0xF8) | 1
        stride = addr("wPartyMon2") - addr("wPartyMon1")
        p.memory[addr("wPartyCount")] = 2
        p.memory[addr("wPartySpecies"):addr("wPartySpecies") + 3] = [1, 16, 255]
        for index, species, level, moves in [
            (0, 1, 10, [33, 73, 22, 250 if full_moves else 0]),
            (1, 16, 7, [33, 0, 0, 0]),
        ]:
            base = addr("wPartyMon1") + stride * index
            p.memory[base:base + stride] = [0] * stride
            p.memory[base] = species
            p.memory[addr("wPartyMon1Level") + stride * index] = level
            moveaddr = addr("wPartyMon1Moves") + stride * index
            p.memory[moveaddr:moveaddr + 4] = moves
            ppaddr = addr("wPartyMon1PP") + stride * index
            p.memory[ppaddr:ppaddr + 4] = [35, 10, 10, 10 if full_moves else 0]
            for stat in ["HP", "MaxHP", "Attack", "Defense", "Speed", "SpclAtk", "SpclDef"]:
                pointer = addr("wPartyMon1" + stat) + stride * index
                p.memory[pointer:pointer + 2] = [0, 20]
            pointer = addr("wPartyMonNicknames") + 11 * index
            p.memory[pointer:pointer + 11] = [0x93, 0x84, 0x92, 0x93, 0x50, 0, 0, 0, 0, 0, 0]
        self.press("up", 10)

    def press(self, button, frames=100):
        self.p.button_press(button)
        self.p.tick(1 if button == "a" else 8)
        self.p.button_release(button)
        self.p.tick(frames)

    def until(self, name, count, button="a", maximum=30):
        for _ in range(maximum):
            if self.counts.get(name, 0) >= count:
                return
            self.press(button)
        self.snap("failure-" + name.replace(".", "-"))
        raise AssertionError((name, count, self.counts, self.p.register_file.PC))

    def snap(self, name):
        self.p.screen.image.save("work/v4-tito-" + name + ".png")

    def speak(self):
        self.until("TitoXeluisServices.WaitMainMenu", 1)
        self.p.tick(120)

    def used(self):
        flag = 400 + 0x31  # LANDMARK_VIRIDIAN_CITY
        return bool(self.p.memory[addr("wEventFlags") + flag // 8] & (1 << (flag % 8)))

    def close(self):
        self.p.stop(save=False)




def open_trades(c):
    c.speak()
    for button in ['down'] * 4 + ['a']:
        c.press(button, 30)
    for button in ['down', 'down', 'a']:
        c.press(button, 30)
    c.p.tick(200)


def list_rows(c):
    """Scroll the whole list and return every distinct row (without the cursor)."""
    seen = []
    for _ in range(40):
        for line in screen_rows(c.p)[1:11]:
            text = line.replace('│', '').replace('▶', '').strip()
            if text and text not in seen:
                seen.append(text)
        c.press('down', 10)
    return seen


c = Center()
try:
    open_trades(c)
    c.snap('trades-start')
    first = ' '.join(screen_rows(c.p))
    check('TRUEQUES opens a list that starts with the first TITO city', 'T:PUEBLO AZALEA' in first)
    check('and the prompt tells what T: means', 'T: es TITO' in first)
    rows = list_rows(c)
    tito = [r for r in rows if r.startswith('T:')]
    npc = [r for r in rows if ':' in r and not r.startswith('T:')]
    check('all 22 Tito cities are listed with readable names (no garbage glyphs)', len(tito) == 22 and not any('?' in r for r in tito))
    check('and the six NPCs with where to find them',
          sorted(npc) == sorted(['MIKE:ALMACÉN', 'KYLE:CD. MALVA', 'TIM:CD. OLIVO', 'EMY:CD. ENDRINO', 'KIM:RUTA 14', 'FOREST:CENTRAL']))
    check('every row fits the menu (17 columns or fewer)', all(len(r) <= 17 for r in tito + npc))
finally:
    c.close()

# the Viridian trade is already used and Kyle has traded: both rows are gone
c = Center()
try:
    flag = 400 + 0x31  # the Viridian landmark, as in the Tito service test
    c.p.memory[addr('wEventFlags') + flag // 8] |= 1 << (flag % 8)
    c.p.memory[addr('wTradeFlags')] |= 1 << 1
    open_trades(c)
    rows = list_rows(c)
    check('a used city and a finished NPC trade leave the list (21 TITO cities, five NPCs)',
          len([r for r in rows if r.startswith('T:')]) == 21 and not any(r.startswith('KYLE') for r in rows)
          and any(r.startswith('MIKE') for r in rows))
    for _ in range(3):
        c.press('b', 60)
    c.p.tick(120)
    check('leaving the list returns to TITO\'s menu', c.counts.get('TitoXeluisServices.WaitMainMenu', 0) >= 2)
finally:
    c.close()

report = {'passed': len(results), 'tests': results}
Path('work/v56-tito-ui-tests.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
