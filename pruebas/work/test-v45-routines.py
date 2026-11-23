"""v4.5 routines run on the real compiled ROM (PyBoy CPU harness): infinite combat items,
hatching into a random shiny first-stage Pokemon, the Super League species picker and the
10-step egg counter."""
import json
import re
import sys
from pathlib import Path

sys.argv = [sys.argv[0], 'work/source/pokecristal.gbc']
sys.path.insert(0, 'work')
import cpu_harness as h

root = Path('work/source')
tests = []


def check(name, condition=True):
    assert condition, name
    tests.append({'name': name, 'passed': True})
    print('PASS', name, flush=True)


addr = h.addr
const = (root / 'constants/pokemon_constants.asm').read_text(encoding='utf8')
species = re.findall(r'^\s*const ([A-Z][A-Z0-9_]+)\s*(?:;[^\n]*)?$', const, re.M)[:252]
ids = {name: i + 1 for i, name in enumerate(species)}
assert ids['CELEBI'] == 251 and ids['DARK_LUGIA'] == 252

evos = (root / 'data/pokemon/evos_attacks.asm').read_text(encoding='utf8')
normal = {re.sub('[^A-Z0-9]', '', mon): mon for mon in species}
has_evolution, parents = set(), {}
for name, body in re.findall(r'^(\w+)EvosAttacks:\n(.*?)(?=^\w+EvosAttacks:|\Z)', evos, re.M | re.S):
    mon = normal[name.upper()]
    first = body.splitlines()[0].strip()
    if not first.startswith('db 0'):
        has_evolution.add(mon)
    for child in re.findall(r'^\s*db EVOLVE_\w+, (?:[^\n,]+, )?([A-Z][A-Z0-9_]+)\s*$', body, re.M):
        parents[child] = mon
bst = {}
for mon in species:
    text = (root / 'data/pokemon/base_stats' / (mon.lower() + '.asm')).read_text(encoding='utf8')
    bst[mon] = sum(map(int, re.search(r'^\s*db\s+(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)', text, re.M).groups()))
LEGENDS = {'ARTICUNO', 'ZAPDOS', 'MOLTRES', 'MEWTWO', 'MEW', 'RAIKOU', 'ENTEI', 'SUICUNE', 'LUGIA', 'HO_OH', 'CELEBI', 'DARK_LUGIA'}


def base_stage(mon):
    while mon in parents:
        mon = parents[mon]
    return mon


r = h.Routine()

# --- Infinite held items ----------------------------------------------------------------------------
FOCUS_SASH, CHOICE_BAND, CHOICE_SPECS, CHOICE_SCARF, LEFTOVERS, POTION = 0x19, 0x2d, 0x32, 0x5a, 0x92, 0x12
infinite = []
for item in range(1, 256):
    result = r.run('IsInfiniteHeldItem', A=item)
    if result['F'] & 0x10:
        infinite.append(item)
check('exactly Focus Sash, Choice Band, Choice Specs, Choice Scarf and Leftovers are infinite',
      infinite == sorted([FOCUS_SASH, CHOICE_BAND, CHOICE_SPECS, CHOICE_SCARF, LEFTOVERS]))


def bag(r_, items):
    r_.write('wNumItems', len(items))
    base = addr('wItems')
    flat = [x for pair in items for x in pair] + [255]
    r_.p.memory[base:base + len(flat)] = flat


def count(r_, item):
    n = r_.p.memory[addr('wNumItems')]
    raw = list(r_.p.memory[addr('wItems'):addr('wItems') + n * 2])
    return {raw[i * 2]: raw[i * 2 + 1] for i in range(n)}.get(item, 0)


def setup_bag(r_):
    bag(r_, [(CHOICE_BAND, 10), (POTION, 10)])
    r_.write('wCurItem', CHOICE_BAND)
    r_.write('wItemQuantityChange', 1)


r.run('_GiveItemToPokemon', setup_bag, A=0)
check('giving an infinite item to a Pokemon leaves the bag stack at 10', count(r, CHOICE_BAND) == 10)


def setup_potion(r_):
    bag(r_, [(CHOICE_BAND, 10), (POTION, 10)])
    r_.write('wCurItem', POTION)


r.run('_GiveItemToPokemon', setup_potion, A=0)
check('a normal item is still consumed when given', count(r, POTION) == 9)


def setup_take(r_):
    bag(r_, [(CHOICE_BAND, 10)])
    r_.write('wCurItem', CHOICE_BAND)


r.run('_ReceiveItemFromPokemon', setup_take, A=0)
check('taking an infinite item back does not grow the stack', count(r, CHOICE_BAND) == 10)


def setup_take_missing(r_):
    bag(r_, [(POTION, 10)])
    r_.write('wCurItem', CHOICE_BAND)


r.run('_ReceiveItemFromPokemon', setup_take_missing, A=0)
check('taking an infinite item back creates the stack when the bag lacks it', count(r, CHOICE_BAND) == 1)

# --- Hatching ------------------------------------------------------------------------------------------
STRIDE = addr('wPartyMon2') - addr('wPartyMon1')
picked = set()
for run in range(160):
    def setup_hatch(r_):
        r_.write('wPartyCount', 1)
        r_.write('wCurPartyMon', 0)
        base = addr('wPartyMon1')
        r_.p.memory[base:base + STRIDE] = [0] * STRIDE
        r_.p.memory[base] = ids['RATTATA']
        r_.p.memory[addr('wPartyMon1Level')] = 5
    r.run('RerollHatchedEgg', setup_hatch)
    mon = r.p.memory[addr('wPartyMon1')]
    dvs = list(r.p.memory[addr('wPartyMon1DVs'):addr('wPartyMon1DVs') + 2])
    exp = list(r.p.memory[addr('wPartyMon1Exp'):addr('wPartyMon1Exp') + 3])
    name = species[mon - 1]
    assert 1 <= mon <= 251 and name not in LEGENDS, (run, name)
    assert base_stage(name) == name, (run, name)
    assert dvs[1] == 0xaa and (dvs[0] & 0x0f) == 0x0a and ((dvs[0] >> 4) in (2, 3, 6, 7, 10, 11, 14, 15)), (run, dvs)
    assert exp != [0, 0, 0], (run, exp)
    picked.add(name)
check('160 hatchings give a non-legendary first-stage species with shiny DVs and the level-5 experience', len(picked) > 40)

# --- A forced-shiny gift that goes straight to the PC -----------------------------------------------------
sys.path.insert(0, 'work')
from story_helper import EVENTS
force = EVENTS['EVENT_FORCE_SHINY_GIFT']


def setup_box_gift(r_):
    r_.p.memory[addr('wEventFlags') + force // 8] |= 1 << (force % 8)
    r_.p.memory[addr('wEnemyMonDVs'):addr('wEnemyMonDVs') + 2] = [0x12, 0x34]


r.run('BoxGiftRollShiny', setup_box_gift)
dvs = list(r.p.memory[addr('wEnemyMonDVs'):addr('wEnemyMonDVs') + 2])
check('a forced-shiny gift sent to the PC gets shiny DVs', dvs[1] == 0xaa and (dvs[0] & 0x0f) == 0x0a and ((dvs[0] >> 4) in (2, 3, 6, 7, 10, 11, 14, 15)))

# --- Super League species picker -------------------------------------------------------------------
class_ids = {}
trainer_text = (root / 'constants/trainer_constants.asm').read_text(encoding='utf8')
index = 0
current = None
consts = {}
for line in trainer_text.splitlines():
    m = re.match(r'\s*trainerclass (\w+)', line)
    if m:
        index += 1
        consts[m[1]] = index
        current = m[1]
        sub = 0
        continue
    m = re.match(r'\s*const (\w+)', line)
    if m and current:
        sub += 1
        consts[m[1]] = sub
BLUE, RED, CHAMPION, ULEX = consts['BLUE'], consts['RED'], consts['CHAMPION'], consts['ULEX']
chosen = []
for run in range(300):
    cls, tid = [(BLUE, consts['BLUE_SUPER']), (RED, consts['RED_SUPER']), (CHAMPION, consts['LANCE_SUPER']), (ULEX, consts['ULEX_SUPER'])][run % 4]
    previous = list(range(1, 1 + (run // 4) % 6)) if False else []

    def setup_pick(r_):
        r_.write('wOtherTrainerClass', cls)
        r_.write('wOtherTrainerID', tid)
        r_.write('wOTPartyCount', 0)
        r_.write('wCurPartySpecies', ids['MEW'])
    r.run('SuperLeagueRandomizeSpecies', setup_pick)
    mon = r.p.memory[addr('wCurPartySpecies')]
    name = species[mon - 1]
    assert mon <= 251 and name not in has_evolution and bst[name] >= 500, (run, name, bst[name])
    chosen.append(mon)
check('300 Super League picks (the first slots) are fully evolved, at least 500 base total and never Dark Lugia', len(set(chosen)) > 20)


def setup_other(r_):
    r_.write('wOtherTrainerClass', BLUE)
    r_.write('wOtherTrainerID', 1)
    r_.write('wOTPartyCount', 0)
    r_.write('wCurPartySpecies', ids['MEW'])


r.run('SuperLeagueRandomizeSpecies', setup_other)
check('the regular AZUL party keeps its authored species', r.p.memory[addr('wCurPartySpecies')] == ids['MEW'])

taken = [ids['MEWTWO'], ids['SNORLAX'], ids['DRAGONITE'], ids['TYRANITAR'], ids['MACHAMP']]
repeats = 0
for run in range(120):
    def setup_dupes(r_):
        r_.write('wOtherTrainerClass', BLUE)
        r_.write('wOtherTrainerID', consts['BLUE_SUPER'])
        r_.write('wOTPartyCount', len(taken))
        r_.p.memory[addr('wOTPartySpecies'):addr('wOTPartySpecies') + len(taken)] = taken
    r.run('SuperLeagueRandomizeSpecies', setup_dupes)
    if r.p.memory[addr('wCurPartySpecies')] in taken:
        repeats += 1
check('the Super League picker never repeats a Pokemon already on the enemy team', repeats == 0)

# --- 10-step eggs ----------------------------------------------------------------------------------
EGG = 253


def egg_with(value):
    def setup(r_):
        r_.write('wPartyCount', 2)
        r_.p.memory[addr('wPartySpecies'):addr('wPartySpecies') + 3] = [ids['PIKACHU'], EGG, 255]
        r_.p.memory[addr('wPartyMon1Happiness')] = 70
        r_.p.memory[addr('wPartyMon1Happiness') + STRIDE] = value
    return setup


def after(value):
    result = r.run('DoEggStep', egg_with(value))
    return r.p.memory[addr('wPartyMon1Happiness') + STRIDE], (result['F'] & 0x80) == 0  # (counter, hatch-ready)


check('a 120-cycle egg is clamped to 10 by its first step', after(120) == (9, False))
check('an egg with 10 steps left needs nine more', after(10) == (9, False))
check('an egg with one step left is ready to hatch', after(1) == (0, True))
check('the happiness of a Pokemon that is not an egg is untouched', r.p.memory[addr('wPartyMon1Happiness')] == 70)

report = {'passed': len(tests), 'tests': tests}
Path('work/v45-routines-tests.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
r.close()
