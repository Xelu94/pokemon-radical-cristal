"""v5.7 changes played in the emulator: the Super League champion's prize when the party is full (it goes to the PC,
or, with no room anywhere, the player is sent out of the room with the prize still waiting), and the Dark Lugia
back sprite being the one supplied by the author."""
import json
import os
import re
import sys
from pathlib import Path

base = Path('work/test-v43-changes.py').read_text(encoding='utf8')
exec(base[:base.index('# --- Starting inventory')])   # check(), maps, items and Game
sys.path.insert(0, 'work')
from story_helper import StoryMixin, EVENTS

src = Path('work/test-v55-story.py').read_text(encoding='utf8')
exec(src[src.index('class G('):src.index('girl = os.environ')])   # G, strong_party, quiet, mash

girl = os.environ.get('PLAYER_GENDER') == '1'
center = maps['INDIGO_PLATEAU_POKECENTER_1F']


def prize(party_full, pc_full):
    g = G('SUPER_LEAGUE_TITO', 4, 22)
    strong_party(g)
    if party_full:
        stride = g.a('wPartyMon2') - g.a('wPartyMon1')
        g.write('wPartyCount', 6)
        g.p.memory[g.a('wPartySpecies'):g.a('wPartySpecies') + 7] = [150, 16, 19, 21, 23, 25, 255]
        for i in range(1, 6):
            base_ = g.a('wPartyMon1') + stride * i
            g.p.memory[base_:base_ + stride] = [0] * stride
            g.p.memory[base_] = [16, 19, 21, 23, 25][i - 1]
            g.p.memory[g.a('wPartyMon1Level') + stride * i] = 30
            g.p.memory[g.a('wPartyMon1Moves') + stride * i] = 33
            g.p.memory[g.a('wPartyMon1PP') + stride * i] = 35
            for stat in ['HP', 'MaxHP', 'Attack', 'Defense', 'Speed', 'SpclAtk', 'SpclDef']:
                p_ = g.a('wPartyMon1' + stat) + stride * i
                g.p.memory[p_:p_ + 2] = [0, 90]
    counts = {'box': 0, 'failed': 0}
    g.p.hook_register(*g.symbols['SendMonIntoBox'], lambda _: counts.__setitem__('box', counts['box'] + 1), None)
    g.p.hook_register(*g.symbols['GivePoke.FailedToGiveMon'], lambda _: counts.__setitem__('failed', counts['failed'] + 1), None)
    if pc_full:
        # the instruction after "call SendMonIntoBox" is "jp nc, .FailedToGiveMon": make the call report a full box
        bank, start = g.symbols['GivePoke.failed']
        data = g.rom
        off = bank * 0x4000 + start - 0x4000
        target = g.symbols['SendMonIntoBox'][1]
        needle = bytes([0xcd, target & 255, target >> 8])
        at = data.index(needle, off, off + 80)
        after = start + (at - off) + 3

        def full(_):
            g.p.register_file.F &= ~0x10
        g.p.hook_register(bank, after, full, None)
    g.set_event('EVENT_BEAT_TITO_XELUIS')
    g.set_event('EVENT_SUPER_BEAT_TITO_ROOM')
    g.p.tick(30)
    for _ in range(24):
        g.press('up', 6, hold=14)
        if g.pos()[1] <= 5:
            break
    g.press('right', 8, hold=14)
    g.press('up', 8, hold=14)
    out = False
    for i in range(300):
        g.press('a', 30, hold=6)
        if i % 5 == 4 and quiet(g) and [g.read('wMapGroup'), g.read('wMapNumber')] == center:
            out = True
            break
    g.p.tick(60)
    return g, counts, out


g, counts, out = prize(party_full=True, pc_full=False)
check('full party: the Charizard goes to the PC, the prize is marked and the player leaves the Super League',
      out and counts['box'] == 1 and counts['failed'] == 0 and g.event('EVENT_SUPER_LEAGUE_BEAT_TITO')
      and g.read('wPartyCount') == 6 and not g.event('EVENT_SUPER_BEAT_TITO_ROOM'))
check('full party: the party kept its own held items (the letter is not attached to someone else)',
      g.p.memory[g.a('wPartyMon6Item')] != 158 and all(g.p.memory[g.a('wPartyMon1Item') + (g.a('wPartyMon2') - g.a('wPartyMon1')) * i] != 158 for i in range(6)))
g.close()

g, counts, out = prize(party_full=True, pc_full=True)
check('no room anywhere: the player is sent out instead of being locked in, and the prize is still pending',
      out and counts['failed'] == 1 and not g.event('EVENT_SUPER_LEAGUE_BEAT_TITO') and g.event('EVENT_SUPER_BEAT_TITO_ROOM')
      and g.read('wPartyCount') == 6)
g.close()

g, counts, out = prize(party_full=False, pc_full=False)
stride = g.a('wPartyMon2') - g.a('wPartyMon1')
check('room in the party: the Charizard joins it with the letter, as before',
      out and counts['box'] == 0 and g.event('EVENT_SUPER_LEAGUE_BEAT_TITO') and g.read('wPartyCount') == 2
      and g.p.memory[g.a('wPartyMon1Item') + stride] == 158)
g.close()

# --- Dark Lugia's back sprite is Lugia's ---------------------------------------------------------------
rom = Path('work/source/pokecristal.gbc').read_bytes()
sym = {}
for line in Path('work/source/pokecristal.sym').read_text().splitlines():
    m = re.match(r'([0-9a-fA-F]+):([0-9a-fA-F]+)\s+(\S+)', line)
    if m:
        sym[m[3]] = (int(m[1], 16), int(m[2], 16))


def blob(name, size):
    bank, address = sym[name]
    off = bank * 0x4000 + address - 0x4000
    return rom[off:off + size]


from PIL import Image
png = Image.open('work/source/gfx/pokemon/dark_lugia/back.png').convert('RGB')
shade = {(255, 255, 255): 0, (99, 82, 140): 1, (66, 41, 90): 2, (0, 0, 0): 3}
check('the Dark Lugia back picture is 48x48 and uses only the four Dark Lugia colours',
      png.size == (48, 48) and set(png.getdata()) <= set(shade))
expected = bytearray()
for tx in range(6):          # the pictures are built with --columns: tiles go down each column first
    for ty in range(6):
        for row in range(8):
            lo = hi = 0
            for col in range(8):
                v = shade[png.getpixel((tx * 8 + col, ty * 8 + row))]
                lo = (lo << 1) | (v & 1)
                hi = (hi << 1) | (v >> 1)
            expected += bytes([lo, hi])
check('and the built 2bpp data is exactly that picture', bytes(expected) == Path('work/source/gfx/pokemon/dark_lugia/back.2bpp').read_bytes())
packed = Path('work/source/gfx/pokemon/dark_lugia/back.2bpp.lz').read_bytes()
check('and the ROM carries that picture (the packed data sits at DarkLugiaBackpic)', blob('DarkLugiaBackpic', len(packed)) == packed)
check('it is no longer the Lugia picture', blob('DarkLugiaBackpic', len(packed)) != blob('LugiaBackpic', len(packed)))

report = {'passed': len(tests), 'tests': tests}
Path('work/v57-story-girl-tests.json' if girl else 'work/v57-story-tests.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
