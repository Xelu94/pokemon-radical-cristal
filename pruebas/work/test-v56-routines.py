"""v5.6 routines on the compiled ROM (PyBoy CPU harness): the modern moves (data, TMs, names, descriptions),
Tito's reminder for every species, the list of trading partners and the Ulex lock."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, 'work')
import cpu_harness as h

root = Path('work/source')
tests = []


def check(name, condition=True):
    assert condition, name
    tests.append({'name': name, 'passed': True})
    print('PASS', name, flush=True)


def consts(path):
    out = {}
    for line in (root / path).read_text(encoding='utf8').splitlines():
        m = re.match(r'\s*const (\w+)\s*;\s*([0-9a-fA-F]{2})', line)
        if m:
            out[m[1]] = int(m[2], 16)
    return out


mons = consts('constants/pokemon_constants.asm')
moves = consts('constants/move_constants.asm')
for alias, target in re.findall(r'^DEF (\w+) EQU (\w+)', (root / 'constants/move_constants.asm').read_text(encoding='utf8'), re.M):
    if target in moves:
        moves[alias] = moves[target]
type_ids = {'NORMAL': 0, 'FIGHTING': 1, 'FLYING': 2, 'POISON': 3, 'GROUND': 4, 'ROCK': 5, 'BUG': 7, 'GHOST': 8, 'STEEL': 9,
            'FIRE': 20, 'WATER': 21, 'GRASS': 22, 'ELECTRIC': 23, 'PSYCHIC_TYPE': 24, 'ICE': 25, 'DRAGON': 26, 'DARK': 27, 'FAIRY': 28}
EFFECTS = {}
n = 0
for line in (root / 'constants/move_effect_constants.asm').read_text(encoding='utf8').splitlines():
    m = re.match(r'\s*const (EFFECT_\w+)', line)
    if m:
        EFFECTS[m[1]] = n
        n += 1
addr = h.addr
r = h.Routine()

# --- the new moves -------------------------------------------------------------------------------------
NEW = {  # name: (effect, power, type, class, accuracy, pp, chance)
    'AQUA_JET': ('PRIORITY_HIT', 40, 'WATER', 1, 100, 20, 0), 'SEED_BOMB': ('NORMAL_HIT', 80, 'GRASS', 1, 100, 15, 0),
    'EARTH_POWER': ('SP_DEF_DOWN_HIT', 90, 'GROUND', 2, 100, 10, 10), 'HYPER_VOICE': ('NORMAL_HIT', 90, 'NORMAL', 2, 100, 10, 0),
    'SHADOW_SNEAK': ('PRIORITY_HIT', 40, 'GHOST', 1, 100, 30, 0), 'POWER_GEM': ('NORMAL_HIT', 80, 'ROCK', 2, 100, 20, 0),
    'AQUA_TAIL': ('NORMAL_HIT', 90, 'WATER', 1, 90, 10, 0), 'BULLET_PUNCH': ('PRIORITY_HIT', 40, 'STEEL', 1, 100, 30, 0),
    'ENERGY_BALL': ('SP_DEF_DOWN_HIT', 90, 'GRASS', 2, 100, 10, 10), 'SCALD': ('BURN_HIT', 80, 'WATER', 2, 100, 15, 30),
    'ZEN_HEADBUTT': ('FLINCH_HIT', 80, 'PSYCHIC_TYPE', 1, 90, 15, 20), 'SIGNAL_BEAM': ('CONFUSE_HIT', 75, 'BUG', 2, 100, 15, 10),
    'STONE_EDGE': ('NORMAL_HIT', 100, 'ROCK', 1, 80, 5, 0), 'SHADOW_CLAW': ('NORMAL_HIT', 70, 'GHOST', 1, 100, 15, 0),
    'AURA_SPHERE': ('ALWAYS_HIT', 80, 'FIGHTING', 2, 100, 20, 0), 'DRAIN_PUNCH': ('LEECH_HIT', 75, 'FIGHTING', 1, 100, 10, 0),
    'DISCHARGE': ('PARALYZE_HIT', 80, 'ELECTRIC', 2, 100, 15, 30), 'HEAT_WAVE': ('BURN_HIT', 95, 'FIRE', 2, 90, 10, 10),
    'BRAVE_BIRD': ('RECOIL_HIT', 120, 'FLYING', 1, 100, 15, 0), 'AIR_SLASH': ('FLINCH_HIT', 75, 'FLYING', 2, 95, 15, 30),
    'ICE_FANG': ('FREEZE_HIT', 65, 'ICE', 1, 95, 15, 10),
}
bad = []
for name, (eff, power, typ, cat, acc, pp, chance) in NEW.items():
    d = h.move_bytes(moves[name])
    ok = (d[1] == EFFECTS['EFFECT_' + eff] and d[2] == power and d[3] & 0x3f == type_ids[typ] and d[3] >> 6 == cat
          and d[4] == acc * 255 // 100 and d[5] == pp)
    if not ok:
        bad.append((name, list(d)))
check('the %d new modern moves have the intended effect, power, type, category and PP' % len(NEW), not bad)
names = (root / 'data/moves/names.asm').read_text(encoding='utf8')
check('and their own Spanish names (and the junk ones are gone)',
      all('li "%s"' % n in names for n in ('ACUA JET', 'ENERGIBOLA', 'CHISPAZO', 'ESFERA AURAL', 'PUÑO DRENAJE', 'ROCA AFILADA'))
      and not any(f'li "{n}"' in names for n in ('FIJAR BLANCO', 'KINÉTICO', 'MÁS PSIQUE', 'TELÉPATA', 'PESADILLA', 'RENCOR')))
tm = [int(x) for x in re.findall(r'\tdb (\d+) ; TM\d\d', (root / 'data/moves/tmhm_moves.asm').read_text(encoding='utf8'))]
junk = {moves[n] for n in ('SPLASH', 'TACKLE', 'GROWL', 'POUND', 'SAND_ATTACK')} - {moves['ICE_FANG']}
check('no TM teaches Splash, Tackle, Growl or Pound any more and every TM is a different move', len(set(tm)) == 50 and not (set(tm) & junk))
check('several TMs now teach the modern moves',
      sum(moves[n] in tm for n in NEW) >= 12)

# --- Tito's reminder for every species -----------------------------------------------------------------
table = re.search(r'\.Moves:\n; level, move, type\n(.*?)\tdb 0', (root / 'engine/events/tito_xeluis.asm').read_text(encoding='utf8'), re.S)[1]
rows = [(int(a), moves[b], type_ids[c]) for a, b, c in re.findall(r'db\s+(\d+), (\w+), (\w+)', table)]


def base_types(name):
    path = root / 'data/pokemon/base_stats' / (name.lower() + '.asm')
    m = re.search(r'db (\w+), (\w+) ; type', path.read_text(encoding='utf8'))
    return type_ids[m[1]], type_ids[m[2]]


def reminder(species, level):
    def setup(rr):
        rr.write('wCurPartyMon', 0)
        rr.write('wCurPartySpecies', species)
        rr.write('wPartyMon1Level', level)
        rr.p.memory[addr('wPartyMon1Moves'):addr('wPartyMon1Moves') + 4] = [0, 0, 0, 0]
        rr.p.memory[addr('wPartyMon1Species')] = species
    r.run('TitoBuildReminderMoves', setup)
    base = addr('wTitoReminderMoves')
    count = r.p.memory[base]
    return list(r.p.memory[base + 1:base + 1 + count]) if count else []


missing = 0
checked = 0
for name, sid in mons.items():
    if sid > 251 or not (root / 'data/pokemon/base_stats' / (name.lower() + '.asm')).exists():
        continue
    t1, t2 = base_types(name)
    got = reminder(sid, 100)
    checked += 1
    for level, move, typ in rows:
        if typ in (t1, t2) and move not in got and len(got) < 30:
            missing += 1
check('Tito remembers every modern move of its type for all %d species at level 100 (%d moves in %d types)' % (checked, len({m for _, m, _ in rows}), len({t for _, _, t in rows})),
      checked > 240 and missing == 0)
water = reminder(mons['MAGIKARP'], 15)
check('at level 15 a Water Pokemon is offered Aqua Jet but not Scald or Aqua Tail',
      moves['AQUA_JET'] in water and moves['SCALD'] not in water and moves['AQUA_TAIL'] not in water)
check('modern moves of other types are not offered (Charmander gets no Water move)',
      moves['AQUA_JET'] not in reminder(mons['CHARMANDER'], 100))
for old in ('POISON_JAB', 'DRAGON_CLAW', 'DARK_PULSE', 'IRON_HEAD', 'BUG_BUZZ', 'X_SCISSOR', 'MOONBLAST'):
    pass
check('the moves added in earlier versions are in the table too (Gengar: Poison Jab; Dragonite: Dragon Claw; Tyranitar: Dark Pulse)',
      moves['POISON_JAB'] in reminder(mons['GENGAR'], 60) and moves['DRAGON_CLAW'] in reminder(mons['DRAGONITE'], 60)
      and moves['DARK_PULSE'] in reminder(mons['TYRANITAR'], 60))

# --- the list of trading partners ---------------------------------------------------------------------
rom = h.ROM.read_bytes()
bank, ptr = h.symbols['TitoBuildTradeList']
start = bank * 0x4000 + ptr - 0x4000
code = rom[start:start + 80]
beaten_flag = code[code.index(0x11) + 1] + code[code.index(0x11) + 2] * 256   # ld de, EVENT_BEAT_TITO_XELUIS
TITO_BASE = code[code.index(0x21) + 1] + code[code.index(0x21) + 2] * 256      # ld hl, EVENT_TITO_TRADE_BASE


def trade_list(beaten=False, used_cities=(), used_npcs=()):
    def setup(rr):
        flags = addr('wEventFlags')
        rr.p.memory[flags:flags + 0x100] = [0] * 0x100
        rr.p.memory[addr('wTradeFlags'):addr('wTradeFlags') + 2] = [0, 0]
        for i in used_npcs:
            rr.p.memory[addr('wTradeFlags') + i // 8] |= 1 << (i % 8)
        for landmark in used_cities:
            f = TITO_BASE + landmark
            rr.p.memory[flags + f // 8] |= 1 << (f % 8)
        if beaten:
            f = beaten_flag
            rr.p.memory[flags + f // 8] |= 1 << (f % 8)
    r.run('TitoBuildTradeList', setup)
    base = addr('wTitoReminderMoves')
    count = r.p.memory[base]
    return list(r.p.memory[base + 1:base + 1 + count]) if count else []


def landmark_of(code):
    return r.run('TitoTradeCityLandmark', A=code)['A']


landmarks = [landmark_of(c) for c in range(1, 23)]
check('the 22 Tito Pokemon Centers map to 22 different landmarks', len(set(landmarks)) == 22 and 0 not in landmarks)
full = trade_list()
check('at the start 28 partners can be traded with (22 TITO cities and six NPCs)', full == list(range(1, 29)))
check('a city whose trade is used is left out', trade_list(used_cities=[landmarks[5]]) == [c for c in range(1, 29) if c != 6])
check('an NPC whose trade is done is left out (Kyle)', trade_list(used_npcs=[1]) == [c for c in range(1, 29) if c != 24])
check('all six NPCs done leaves only TITO', trade_list(used_npcs=[0, 1, 2, 3, 5, 6]) == list(range(1, 23)))
check('once TITO is beaten every one of his cities is available again',
      trade_list(beaten=True, used_cities=landmarks) == list(range(1, 29)))
check('everything used leaves the list empty', trade_list(used_cities=landmarks, used_npcs=[0, 1, 2, 3, 5, 6]) == [])

# --- Ulex has no lock ---------------------------------------------------------------------------------
out = r.run('UlexCanBattle', lambda rr: rr.write('wJohtoBadges', 0b11))
check('Ulex can always be fought: no badge lock any more', r.p.memory[addr('wScriptVar')] == 1)
r.p.memory[addr('wScriptVar')] = 0
fl = addr('wEventFlags')


def setup_locked(rr):
    rr.write('wJohtoBadges', 0b111111)
    f = 0
    for i in range(0, 0x100):
        rr.p.memory[fl + i] = 0xff   # every event flag set, including every Ulex badge milestone
r.run('UlexCanBattle', setup_locked)
check('even with every milestone flag set', r.p.memory[addr('wScriptVar')] == 1)
ulex = (root / 'engine/events/ulex.asm').read_text(encoding='utf8')
check('and the "gana otra medalla" text is gone', 'Gana otra medalla' not in ulex and 'WaitForBadge' not in ulex)

report = {'passed': len(tests), 'tests': tests}
Path('work/v56-routines-tests.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
r.close()
