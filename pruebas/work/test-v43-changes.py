"""v4.3 changes on the real compiled ROM: HM Fly in the party menu, Map Card
scene, no healing items in marts, League supplies, infinite 99 Rare Candies and
the pocket labels / circular navigation of the bag."""
import io
import os
import json
import re
from pathlib import Path
from pyboy import PyBoy

root = Path('work/source')
tests = []


def check(name, condition=True):
    assert condition, name
    tests.append({'name': name, 'passed': True})
    print('PASS', name, flush=True)


maps = {}
group = number = 0
for line in (root/'constants/map_constants.asm').read_text(encoding='utf8').splitlines():
    if re.match(r'\s*newgroup ', line):
        group += 1
        number = 0
    match = re.match(r'\s*map_const (\w+)', line)
    if match:
        number += 1
        maps[match[1]] = [group, number]

items = {}
for line in (root/'constants/item_constants.asm').read_text(encoding='utf8').splitlines():
    match = re.match(r'\s*const (\w+)\s*; ([0-9a-f]{2})\s*$', line)
    if match:
        items.setdefault(match[1], int(match[2], 16))


class Game:
    def __init__(self, mapname, x, y):
        rom = root/'pokecristal.gbc'
        self.symbols = {}
        for line in rom.with_suffix('.sym').read_text().splitlines():
            match = re.match(r'([\da-fA-F]+):([\da-fA-F]+)\s+(\S+)', line)
            if match:
                self.symbols[match[3]] = int(match[1], 16), int(match[2], 16)
        self.rom = bytearray(rom.read_bytes())
        data = bytearray(self.rom)
        for name in ['PlayerProfileSetup', 'OakSpeech', 'ShrinkPlayer', '_InitializeStartDay']:
            data[self.offset(name)] = 0xc9
        data[self.offset('Route31CheckMomCallCallback')] = 0x90
        if os.environ.get('PLAYER_GENDER') == '1':
            # the intro is skipped, so a girl is chosen by patching what it would have stored
            address = self.a('wPlayerGender')
            start = self.offset('OakSpeech')
            data[start:start + 6] = bytes([0x3e, 0x01, 0xea, address & 255, address >> 8, 0xc9])
        spawn = self.offset('SpawnPoints')
        data[spawn:spawn+4] = bytes(maps[mapname] + [x, y])
        self.p = PyBoy(io.BytesIO(data), window='null', sound_emulated=False, log_level='ERROR')
        self.p.set_emulation_speed(0)
        self.counts = {}
        self.p.tick(360)
        self.press('start', 120)
        self.press('start', 120)
        self.p.button_press('a'); self.p.tick(32); self.p.button_release('a'); self.p.tick(300)
        self.write('wOptions', (self.read('wOptions') & 0x38) | 0x41)
        self.p.tick(60)

    def texts(self, labels):
        # Map scripts are bytecode: observe the text actually printed on screen.
        self.counts = {label: 0 for label in labels}
        addresses = {self.a(label): label for label in labels}
        def count(_):
            label = addresses.get(self.p.register_file.HL)
            if label:
                self.counts[label] += 1
        self.p.hook_register(*self.symbols['MapTextbox'], count, None)

    def a(self, name): return self.symbols[name][1]
    def offset(self, name):
        bank, pointer = self.symbols[name]
        return bank*16384 + pointer - 16384 if bank else pointer
    def read(self, name): return self.p.memory[self.a(name)]
    def write(self, name, value): self.p.memory[self.a(name)] = value
    def mem(self, name, n): return list(self.p.memory[self.a(name):self.a(name)+n])
    def press(self, button='a', frames=30, hold=8):
        self.p.button_press(button); self.p.tick(hold)
        self.p.button_release(button); self.p.tick(frames)
    def tile(self, x, y): return self.p.memory[self.a('wTilemap') + y*20 + x]
    def bag(self):
        n = self.read('wNumItems')
        raw = self.mem('wItems', n*2 + 1)
        return {raw[i*2]: raw[i*2+1] for i in range(n)}
    def party(self, species, level=30):
        stride = self.a('wPartyMon2') - self.a('wPartyMon1')
        self.write('wPartyCount', len(species))
        self.p.memory[self.a('wPartySpecies'):self.a('wPartySpecies')+len(species)+1] = species + [255]
        for i, mon in enumerate(species):
            base = self.a('wPartyMon1') + stride*i
            self.p.memory[base:base+stride] = [0]*stride
            self.p.memory[base] = mon
            self.p.memory[self.a('wPartyMon1Level') + stride*i] = level
            self.p.memory[self.a('wPartyMon1Moves') + stride*i] = 33
            self.p.memory[self.a('wPartyMon1PP') + stride*i] = 35
            for stat in ['HP', 'MaxHP', 'Attack', 'Defense', 'Speed', 'SpclAtk', 'SpclDef']:
                pointer = self.a('wPartyMon1' + stat) + stride*i
                self.p.memory[pointer:pointer+2] = [0, 90]
    def close(self): self.p.stop(save=False)


# --- Starting inventory and infinite Rare Candies --------------------------
g = Game('ROUTE_31', 21, 14)
bag = g.bag()
check('new game starts with one Rare Candy stack of 99 and five held items in 6 slots',
      g.read('wNumItems') == 6 and bag[items['RARE_CANDY']] == 99 and len(bag) == 6)
g.party([152, 6], level=10)
level_address = g.a('wPartyMon1Level')
g.press('start', 40)
g.press('down', 20)
g.press('a', 60)
g.press('a', 40)
g.press('a', 40)
g.press('a', 60)
g.press('a', 40)
check('using a Rare Candy raises the level', g.p.memory[level_address] > 10)
check('the Rare Candy stack stays at 99 after use', g.bag()[items['RARE_CANDY']] == 99)
g.close()

# --- Several Rare Candies at once ------------------------------------------------------------------------
g = Game('ROUTE_31', 21, 14)
g.party([152, 6], level=10)
level_address = g.a('wPartyMon1Level')
g.press('start', 40)
g.press('down', 20)
g.press('a', 60)
g.press('a', 40)
g.press('a', 40)
g.press('a', 60)
for _ in range(4):
    g.press('up', 12)  # the quantity selector starts at 1
g.press('a', 60)
for _ in range(8):
    g.press('a', 40)
check('choosing 5 in the Rare Candy quantity box raises the level by 5 and keeps the stack at 99',
      g.p.memory[level_address] == 15 and g.bag()[items['RARE_CANDY']] == 99)
g.close()

# --- Bag: pocket labels and circular navigation ----------------------------
g = Game('ROUTE_31', 21, 14)
g.press('start', 40)
g.press('a', 60)
labels = []
sequence = []
for step in range(8):
    pocket, category = g.read('wCurPocket'), g.read('wBagCategory')
    sequence.append((pocket, category))
    if pocket == 0:
        labels.append([g.tile(x, 8) for x in range(5)])
    g.press('right', 20)
check('the black pocket box shows the category label tiles MEDICINA, BAYAS, COMBATE and OTROS',
      labels[:4] == [[0x60 + 5*k + i for i in range(5)] for k in range(4)] and labels[4] == labels[0])
check('pressing right cycles MEDICINA, BAYAS, COMBATE, OTROS, then the other pockets and back to MEDICINA',
      [c for p, c in sequence if p == 0] == [1, 2, 3, 4, 1] and [p for p, c in sequence] == [0, 0, 0, 0, 1, 2, 3, 0])
g.close()
g = Game('ROUTE_31', 21, 14)
g.press('start', 40)
g.press('a', 60)
sequence = []
for step in range(5):
    sequence.append((g.read('wCurPocket'), g.read('wBagCategory')))
    g.press('left', 20)
check('pressing left from MEDICINA goes TM/HM, KEY ITEMS, BALLS and re-enters ITEMS at OTROS',
      [p for p, c in sequence] == [0, 3, 2, 1, 0] and sequence[4] == (0, 4))
g.close()
# --- Fly from the Pokemon menu ---------------------------------------------
def fly_menu(with_hm):
    game = Game('ROUTE_31', 21, 14)
    game.party([152, 6])
    game.write('wJohtoBadges', 0xff)
    if with_hm:
        game.p.memory[game.a('wTMsHMs') + 51] = 1
    game.press('start', 40)
    game.press('a', 40)
    game.press('a', 40)
    items_ = game.mem('wMonSubmenuItems', 9)
    game.close()
    return items_

fly_id = 2  # MONMENUITEM_FLY
check('the party submenu offers FLY when the HM is in the bag', fly_id in fly_menu(True))
check('the party submenu does not offer FLY without the HM', fly_id not in fly_menu(False))

# --- Map Card handed over without talking ----------------------------------
for row in (6, 7):
    g = Game('ROUTE_29', 2, row)
    g.texts(['GuideGentGiftText', 'GotMapCardText'])
    for _ in range(24):
        g.press('left', 4)
    for step in range(70):
        g.p.tick(30)
        if step >= 6 and step % 2 == 0:
            g.press('a', 20)
    check('row %d: the old man walks up and gives the Map Card on arrival, once' % row,
          g.counts['GuideGentGiftText'] == 1 and g.counts['GotMapCardText'] == 1)
    g.close()

# --- No healing items in any mart ------------------------------------------
healing = ['POTION', 'SUPER_POTION', 'HYPER_POTION', 'MAX_POTION', 'FULL_RESTORE', 'REVIVE', 'MAX_REVIVE',
           'ANTIDOTE', 'BURN_HEAL', 'ICE_HEAL', 'AWAKENING', 'PARLYZ_HEAL', 'FULL_HEAL', 'FRESH_WATER',
           'SODA_POP', 'LEMONADE', 'ENERGYPOWDER', 'ENERGY_ROOT', 'HEAL_POWDER', 'REVIVAL_HERB', 'RAGECANDYBAR']
rom = g.rom
mart_count = len(re.findall(r'^\s*const MART_', (root/'constants/mart_constants.asm').read_text(encoding='utf8'), re.M))
bank = g.symbols['Marts'][0]
table = g.offset('Marts')
healing_ids = {items[n] for n in healing}
names = []
bad = []
empty = []
for index in range(mart_count):
    pointer = rom[table + index*2] | rom[table + index*2 + 1] << 8
    start = bank*16384 + pointer - 16384
    count = rom[start]
    contents = list(rom[start+1:start+1+count])
    names.append(index)
    if rom[start+1+count] != 0xff:
        bad.append((index, 'unterminated'))
    if not contents:
        empty.append(index)
    bad += [(index, c) for c in contents if c in healing_ids]
check('no mart sells potions, revives, status heals or healing drinks (%d marts)' % len(names), not bad)
check('no mart is left empty', not empty)

# --- League supplies from the Victory Road Gate officer ---------------------
g = Game('VICTORY_ROAD_GATE', 10, 12)
g.party([152, 6])
g.write('wJohtoBadges', 0xff)
before = g.bag()
g.press('up', 40, hold=24)
for step in range(60):
    g.press('a', 40, hold=2)
after = g.bag()
check('the officer hands over 8 Max Potions, 10 Hyper Potions and 7 Full Restores with eight badges',
      after.get(items['MAX_POTION']) == 8 and after.get(items['HYPER_POTION']) == 10
      and after.get(items['FULL_RESTORE']) == 7 and all(after[k] == v for k, v in before.items()))
g.close()

report = {'passed': len(tests), 'tests': tests}
Path('work/v43-changes-tests.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
