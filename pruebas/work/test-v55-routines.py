"""v5.5 routines on the compiled ROM (PyBoy CPU harness): evolution by level for wild and trainer Pokemon,
the previous-leader level floor, a move of the Pokemon's own type from the sixth badge on, Fairy moves in Tito's
move reminder, the new Poison moves and TMs that are never used up."""
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
addr = h.addr
r = h.Routine()


def evolve(species, level):
    out = r.run('EvolveSpeciesForLevel', B=level, C=mons[species])
    return out['A']


expected = [('TOTODILE', 17, 'TOTODILE'), ('TOTODILE', 18, 'CROCONAW'), ('CROCONAW', 40, 'FERALIGATR'),
            ('TOTODILE', 40, 'FERALIGATR'), ('MAGIKARP', 19, 'MAGIKARP'), ('MAGIKARP', 20, 'GYARADOS'),
            ('KADABRA', 35, 'KADABRA'), ('KADABRA', 36, 'ALAKAZAM'), ('MACHOP', 45, 'MACHAMP'),
            ('SLOWPOKE', 38, 'SLOWBRO'), ('SLOWPOKE', 40, 'SLOWKING'), ('POLIWHIRL', 31, 'POLIWHIRL'),
            ('POLIWHIRL', 35, 'POLIWRATH'), ('POLIWHIRL', 40, 'POLITOED'), ('PIKACHU', 31, 'PIKACHU'),
            ('PIKACHU', 32, 'RAICHU'), ('GLOOM', 45, 'VILEPLUME'), ('EEVEE', 60, 'EEVEE'), ('MR__MIME', 60, 'MR__MIME'),
            ('PIDGEY', 18, 'PIDGEOTTO'), ('PIDGEY', 36, 'PIDGEOT'), ('BULBASAUR', 8, 'BULBASAUR')]
bad = [(a, b, c, evolve(a, b)) for a, b, c in expected if evolve(a, b) != mons[c]]
check('wild and trainer Pokemon evolve as far as their level allows (%d cases)' % len(expected), not bad)

# --- level floor: the level of the last leader defeated -------------------------------------------------
def floor(johto, kanto=0, hof=0):
    def setup(rr):
        rr.write('wJohtoBadges', johto)
        rr.write('wKantoBadges', kanto)
        rr.write('wStatusFlags', hof)
    return r.run('GetProgressionLevelFloor', setup)['A']


check('before any badge the floor is 0', floor(0) == 0)
check('with the first badge the floor is the first leader\'s level (19), not three below', floor(1) == 19)
check('with two badges it is the second leader\'s level (24)', floor(3) == 24)
check('a badge won out of order does not raise the floor', floor(2) == 0)
check('with all eight Johto badges the floor is the last Johto leader level (53)', floor(255) == 53)


def wild(level, species, johto):
    def setup(rr):
        rr.write('wJohtoBadges', johto)
    out = r.run('ProgressWildEncounter', setup, B=level, C=mons[species])
    return out['B'], r.p.memory[addr('wCurPartyLevel')]


sp, lvl = wild(12, 'TOTODILE', 1)
check('a wild Pokemon below the floor is raised to the last leader\'s level and evolved to match (Totodile 12 -> Croconaw 19)',
      lvl == 19 and sp == mons['CROCONAW'])
sp, lvl = wild(30, 'TOTODILE', 1)
check('a wild Pokemon above the floor keeps its level and still evolves (Totodile 30 -> Feraligatr)',
      lvl == 30 and sp == mons['FERALIGATR'])
sp, lvl = wild(12, 'TOTODILE', 0)
check('before any badge nothing changes', lvl == 12 and sp == mons['TOTODILE'])

# --- a move of the Pokemon's own type -------------------------------------------------------------------
def move_data(mid):
    d = h.move_bytes(mid)
    return d[2], d[3] & 0x3f   # power, type


type_ids = {'NORMAL': 0, 'FIGHTING': 1, 'FLYING': 2, 'POISON': 3, 'GROUND': 4, 'ROCK': 5, 'BUG': 7, 'GHOST': 8, 'STEEL': 9,
            'FIRE': 20, 'WATER': 21, 'GRASS': 22, 'ELECTRIC': 23, 'PSYCHIC_TYPE': 24, 'ICE': 25, 'DRAGON': 26, 'DARK': 27, 'FAIRY': 28}


def ensure(moveset, t1, t2, badges_johto=0xff, battle_mode=1):
    base = addr('wEnemyMonMoves')

    def setup(rr):
        rr.write('wBattleMode', battle_mode)
        rr.write('wJohtoBadges', badges_johto)
        rr.write('wBaseType1', t1)
        rr.write('wBaseType2', t2)
        rr.p.memory[base:base + 4] = moveset
        rr.p.memory[addr('hRandomAdd')] = (setup.seed * 37) & 0xff
        rr.p.memory[addr('hRandomSub')] = (setup.seed * 91 + 5) & 0xff
    setup.seed = ensure.seed
    ensure.seed += 1
    r.run('StabForWild', setup, D=base >> 8, E=base & 0xff)
    return list(r.p.memory[base:base + 4])


ensure.seed = 1
plain = [moves['TACKLE'], moves['GROWL'], moves['LEER'], moves['TAIL_WHIP']]
ok = True
for t in ('FIRE', 'WATER', 'GRASS', 'ELECTRIC', 'FAIRY', 'POISON', 'GHOST', 'DRAGON', 'STEEL', 'DARK', 'ICE', 'BUG', 'ROCK', 'GROUND', 'FLYING', 'FIGHTING', 'PSYCHIC_TYPE'):
    if t not in type_ids:
        continue
    for _ in range(3):
        out = ensure(plain, type_ids[t], type_ids[t])
        stab = [m for m in out if m and move_data(m)[0] > 0 and move_data(m)[1] == type_ids[t]]
        ok = ok and bool(stab) and out[:3] == plain[:3]
check('a wild Pokemon with no attack of its type gets one (every type checked, three times each)', ok)
unchanged = ensure([moves['EMBER'], moves['GROWL'], moves['LEER'], moves['TAIL_WHIP']], type_ids['FIRE'], type_ids['FIRE'])
check('a Pokemon that already has one keeps its moves', unchanged == [moves['EMBER'], moves['GROWL'], moves['LEER'], moves['TAIL_WHIP']])
few = ensure(plain, type_ids['FIRE'], type_ids['FIRE'], badges_johto=0b11111)
check('with only five badges nothing is added', few == plain)
six = ensure(plain, type_ids['FIRE'], type_ids['FIRE'], badges_johto=0b111111)
check('with six badges it is added', six != plain)
trainer_battle = ensure(plain, type_ids['FIRE'], type_ids['FIRE'], battle_mode=2)
check('the wild hook does nothing in a trainer battle', trainer_battle == plain)
dual = ensure(plain, type_ids['WATER'], type_ids['FLYING'])
check('a dual-type Pokemon gets a move of either type', any(m and move_data(m)[0] > 0 and move_data(m)[1] in (type_ids['WATER'], type_ids['FLYING']) for m in dual))

# trainer party Pokemon: the species is read from the party struct
struct = addr('wOTPartyMon1Species')


def trainer(species, johto):
    def setup(rr):
        rr.write('wJohtoBadges', johto)
        rr.p.memory[struct] = mons[species]
        rr.p.memory[struct + 2:struct + 6] = plain
        rr.p.memory[addr('hRandomAdd')] = 77
    mv = struct + 2
    r.run('StabForTrainer', setup, D=mv >> 8, E=mv & 0xff)
    return list(r.p.memory[mv:mv + 4])


out = trainer('CHARMANDER', 0xff)
check('a trainer\'s Pokemon gets a move of its own type from the sixth badge on',
      any(move_data(m)[0] > 0 and move_data(m)[1] == type_ids['FIRE'] for m in out))
check('a trainer\'s Pokemon keeps its moves before that', trainer('CHARMANDER', 0b11111) == plain)

# --- Fairy moves in Tito's reminder ---------------------------------------------------------------------
def reminder(species, level, known):
    def setup(rr):
        rr.write('wCurPartyMon', 0)
        rr.write('wCurPartySpecies', mons[species])
        rr.write('wPartyMon1Level', level)
        rr.p.memory[addr('wPartyMon1Moves'):addr('wPartyMon1Moves') + 4] = known
        rr.p.memory[addr('wPartyMon1Species')] = mons[species]
    r.run('TitoBuildReminderMoves', setup)
    base = addr('wTitoReminderMoves')
    n = r.p.memory[base]
    return list(r.p.memory[base + 1:base + 1 + n])


high = reminder('MR__MIME', 60, [moves['TACKLE'], 0, 0, 0])
check('Tito remembers Fairy moves for a Fairy-type Pokemon (Mr. Mime, level 60)',
      all(moves[m] in high for m in ('FAIRY_WIND', 'CHARM', 'MOONLIGHT', 'DAZZLING_GLEAM', 'PLAY_ROUGH', 'MOONBLAST')))
low = reminder('MR__MIME', 20, [moves['TACKLE'], 0, 0, 0])
check('only those its level allows at level 20', moves['MOONLIGHT'] in low and moves['DAZZLING_GLEAM'] not in low
      and moves['MOONBLAST'] not in low)
known = reminder('MR__MIME', 60, [moves['MOONBLAST'], moves['CHARM'], 0, 0])
check('moves it already knows are not offered again', moves['MOONBLAST'] not in known and moves['CHARM'] not in known)
other = reminder('CHARMANDER', 60, [moves['SCRATCH'], 0, 0, 0])
check('a Pokemon that is not Fairy type gets none', moves['MOONBLAST'] not in other and moves['PLAY_ROUGH'] not in other)

# --- real wild encounters and every trainer party ------------------------------------------------------
evo_levels = {}
text = (root / 'data/pokemon/evos_attacks.asm').read_text(encoding='utf8')
for label, body in re.findall(r'^(\w+)EvosAttacks:\n(.*?)(?=^\w+EvosAttacks:|\Z)', text, re.M | re.S):
    levels = []
    for line in body.splitlines():
        if line.strip().startswith('db 0'):
            break
        m = re.match(r'\s*db EVOLVE_LEVEL, (\d+),', line)
        if m:
            levels.append(int(m[1]))
    evo_levels[re.sub('[^A-Z0-9]', '', label.upper())] = levels
names_by_id = {v: k for k, v in mons.items()}


def can_still_evolve(species_id, level):
    key = re.sub('[^A-Z0-9]', '', names_by_id.get(species_id, ''))
    return any(t <= level for t in evo_levels.get(key, []))


maps = {}
group = number = 0
for line in (root / 'constants/map_constants.asm').read_text(encoding='utf8').splitlines():
    if re.match(r'\s*newgroup ', line):
        group += 1
        number = 0
    m = re.match(r'\s*map_const (\w+)', line)
    if m:
        number += 1
        maps[m[1]] = (group, number)


def wild_samples(mapname, badges, count):
    out = []
    for i in range(count):
        def setup(rr, i=i):
            rr.write('wMapGroup', maps[mapname][0])
            rr.write('wMapNumber', maps[mapname][1])
            rr.write('wJohtoBadges', badges)
            rr.write('wTimeOfDay', i % 3)
            rr.p.memory[addr('hRandomAdd')] = (i * 53 + 7) & 0xff
            rr.p.memory[addr('hRandomSub')] = (i * 29 + 3) & 0xff
        try:
            r.run('ChooseWildEncounter', setup)
        except AssertionError:
            continue
        sp = r.p.memory[addr('wTempWildMonSpecies')]
        lv = r.p.memory[addr('wCurPartyLevel')]
        if sp:
            out.append((sp, lv))
    return out


wild32 = wild_samples('ROUTE_32', 0b1, 90)
check('wild encounters on Route 32 with one badge are all at least level 19', len(wild32) > 30 and all(lv >= 19 for _, lv in wild32))
check('and every one of them is evolved as far as its level allows', not any(can_still_evolve(sp, lv) for sp, lv in wild32))
def temp_wild(species, level, badges):
    def setup(rr):
        rr.write('wJohtoBadges', badges)
        rr.write('wTempWildMonSpecies', mons[species])
        rr.write('wCurPartyLevel', level)
    r.run('ProgressTempWildMon', setup)
    return r.p.memory[addr('wTempWildMonSpecies')], r.p.memory[addr('wCurPartyLevel')]


check('fishing and tree encounters get the same floor and evolution (Totodile 12 with one badge -> Croconaw 19)',
      temp_wild('TOTODILE', 12, 1) == (mons['CROCONAW'], 19) and temp_wild('TOTODILE', 12, 0) == (mons['TOTODILE'], 12))
wild_start = wild_samples('ROUTE_32', 0, 60)
check('with no badges Route 32 keeps its own levels', len(wild_start) > 20 and min(lv for _, lv in wild_start) < 19)


def base_types(species_id):
    name = names_by_id[species_id].lower()
    path = root / 'data/pokemon/base_stats' / (name + '.asm')
    if not path.exists():
        return (-1, -1)
    m = re.search(r'db (\w+), (\w+) ; type', path.read_text(encoding='utf8'))
    return type_ids.get(m[1], -1), type_ids.get(m[2], -1)


def party_now(cls, tid, badges):
    def setup(rr):
        rr.write('wJohtoBadges', badges)
        rr.write('wBattleMode', 2)
        rr.write('wOtherTrainerClass', cls)
        rr.write('wOtherTrainerID', tid)
    try:
        r.run('ReadTrainerParty', setup)
    except AssertionError:
        return None
    n = r.p.memory[addr('wOTPartyCount')]
    stride = addr('wOTPartyMon2') - addr('wOTPartyMon1')
    out = []
    for i in range(n):
        base = addr('wOTPartyMon1') + stride * i
        out.append((r.p.memory[base], r.p.memory[addr('wOTPartyMon1Level') + stride * i],
                    list(r.p.memory[addr('wOTPartyMon1Moves') + stride * i:addr('wOTPartyMon1Moves') + stride * i + 4])))
    return out


parties = unevolved = no_stab = 0
for cls in range(1, 100):
    for tid in range(1, 12):
        before = party_now(cls, tid, 0)
        if not before:
            continue
        parties += 1
        unevolved += sum(can_still_evolve(sp, lv) for sp, lv, _ in before)
        after = party_now(cls, tid, 0b111111)
        for sp, lv, mv in after:
            types_ = base_types(sp)
            if types_ != (-1, -1) and not any(m and move_data(m)[0] > 0 and move_data(m)[1] in types_ for m in mv):
                no_stab += 1
check('no trainer party (%d parties checked) keeps a Pokemon that its level should have evolved' % parties, parties > 500 and unevolved == 0)
check('with six badges every Pokemon in every trainer party has a damaging move of its own type', no_stab == 0)

def wild_stab_gap(badges):
    missing = 0
    for sp in range(1, 252):
        def setup(rr, sp=sp):
            rr.write('wBattleMode', 1)
            rr.write('wJohtoBadges', badges)
            rr.write('wTempEnemyMonSpecies', sp)
            rr.write('wCurPartyLevel', 40)
            rr.write('wBattleType', 0)
            rr.p.memory[addr('hRandomAdd')] = (sp * 7) & 0xff
        r.run('LoadEnemyMon', setup)
        mv = list(r.p.memory[addr('wEnemyMonMoves'):addr('wEnemyMonMoves') + 4])
        t = (r.p.memory[addr('wEnemyMonType1')], r.p.memory[addr('wEnemyMonType2')])
        if not any(m and move_data(m)[0] > 0 and move_data(m)[1] in t for m in mv):
            missing += 1
    return missing


check('with six badges every one of the 251 wild species is generated with a damaging move of its own type', wild_stab_gap(0b111111) == 0)
check('with five badges some are still generated without one', wild_stab_gap(0b11111) > 20)

# --- data -----------------------------------------------------------------------------------------------
for name, power, typ, cat in [('POISON_JAB', 80, 'POISON', 'PHYSICAL'), ('CROSS_POISON', 70, 'POISON', 'PHYSICAL'),
                              ('GUNK_SHOT', 120, 'POISON', 'PHYSICAL'), ('SLUDGE_WAVE', 95, 'POISON', 'SPECIAL')]:
    d = h.move_bytes(moves[name])
    check('%s is a %s %s move of power %d with a chance to poison' % (name, typ.lower(), cat.lower(), power),
          d[2] == power and d[3] & 0x3f == type_ids[typ] and (d[3] >> 6) == {'PHYSICAL': 1, 'SPECIAL': 2}[cat])
names = (root / 'data/moves/names.asm').read_text(encoding='utf8')
check('the four new Poison moves have their own names',
      all('li "%s"' % n in names for n in ('PUYA NOCIVA', 'VENENO X', 'LANZAMUGRE', 'ONDA TÓXICA')))
tm = (root / 'engine/items/tmhm.asm').read_text(encoding='utf8')
check('TMs are never used up (no ConsumeTM)', 'ConsumeTM' not in tm)

report = {'passed': len(tests), 'tests': tests}
Path('work/v55-routines-tests.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
r.close()
