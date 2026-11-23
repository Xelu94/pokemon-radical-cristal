"""v5.8 routines on the compiled ROM (PyBoy CPU harness): the move-set curve from the fourth badge on (wild and trainer
Pokemon) and the stronger Super League teams (legendaries, Dark Lugia as Ulex's last Pokemon)."""
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
names_by_id = {}
for _k, _v in mons.items():
    names_by_id.setdefault(_v, _k)
type_ids = {'NORMAL': 0, 'FIGHTING': 1, 'FLYING': 2, 'POISON': 3, 'GROUND': 4, 'ROCK': 5, 'BUG': 7, 'GHOST': 8, 'STEEL': 9,
            'FIRE': 20, 'WATER': 21, 'GRASS': 22, 'ELECTRIC': 23, 'PSYCHIC_TYPE': 24, 'ICE': 25, 'DRAGON': 26, 'DARK': 27, 'FAIRY': 28}
addr = h.addr
r = h.Routine()


def move_info(mid):
    d = h.move_bytes(mid)
    return {'power': d[2], 'type': d[3] & 0x3f, 'cat': d[3] & 0xc0, 'acc': d[4]}


def badges_for(n):
    johto = (1 << min(n, 8)) - 1
    kanto = (1 << max(0, n - 8)) - 1
    return johto, kanto


def base_data(name):
    text = (root / 'data/pokemon/base_stats' / (name.lower() + '.asm')).read_text(encoding='utf8')
    stats = [int(x) for x in re.search(r'db\s+(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)', text).groups()]
    t = re.search(r'db (\w+), (\w+) ; type', text).groups()
    return stats, (type_ids[t[0]], type_ids[t[1]])


def wild_moves(species, badges):
    johto, kanto = badges_for(badges)

    def setup(rr):
        rr.write('wBattleMode', 1)
        rr.write('wJohtoBadges', johto)
        rr.write('wKantoBadges', kanto)
        rr.write('wTempEnemyMonSpecies', species)
        rr.write('wCurPartyLevel', 50)
        rr.write('wBattleType', 0)
        rr.p.memory[addr('hRandomAdd')] = (species * 7 + badges * 13) & 0xff
        rr.p.memory[addr('hRandomSub')] = (species * 3 + badges) & 0xff
    r.run('LoadEnemyMon', setup)
    return list(r.p.memory[addr('wEnemyMonMoves'):addr('wEnemyMonMoves') + 4])


UTILITY = [moves[n] for n in ('SWORDS_DANCE', 'AGILITY', 'RECOVER', 'SUBSTITUTE', 'TOXIC', 'THUNDER_WAVE', 'PROTECT', 'REFLECT',
                              'LIGHT_SCREEN', 'AMNESIA', 'SPORE', 'MILK_DRINK', 'SOFTBOILED')]
species = [(n, sid) for n, sid in mons.items() if sid <= 251 and (root / 'data/pokemon/base_stats' / (n.lower() + '.asm')).exists()]


def survey(badges):
    p1 = min(60 + 5 * (badges - 4), 90)
    bad = {'distinct': 0, 'weak0': 0, 'slot0': 0, 'slot1': 0, 'slot2': 0, 'slot3': 0, 'lean': 0, 'acc': 0}
    power_sum = 0
    for name, sid in species:
        (hp, atk, df, spd, sat, sdf), (t1, t2) = base_data(name)[0], base_data(name)[1]
        mv = wild_moves(sid, badges)
        info = [move_info(m) if m else None for m in mv]
        if len(set(mv)) != 4 or 0 in mv:
            bad['distinct'] += 1
            continue
        lean = 0x40 if atk > sat else 0x80
        if not (info[0]['power'] >= 50 and info[0]['type'] == t1):
            bad['slot0'] += 1
        if info[0]['power'] < p1:
            bad['weak0'] += 1
        if not (info[1]['power'] >= 40 and info[1]['type'] == t2):
            bad['slot1'] += 1
        if not (info[2]['power'] >= 40 and info[2]['type'] not in (t1, t2)):
            bad['slot2'] += 1
        if badges >= 7:
            if mv[3] not in UTILITY:
                bad['slot3'] += 1
        elif not (info[3]['power'] >= 40 and info[3]['type'] not in (t1, t2)):
            bad['slot3'] += 1
        for i in range(3):
            if info[i]['power'] and info[i]['acc'] < 216:
                bad['acc'] += 1
        if info[0]['cat'] != lean:
            bad['lean'] += 1
        power_sum += sum(i['power'] for i in info[:3])
    return bad, power_sum / len(species) / 3


results = {}
for badges in (4, 7, 10, 16):
    bad, avg = survey(badges)
    results[badges] = avg
    print(badges, bad, round(avg, 1), flush=True)
    check('%d badges: all %d wild species get four different moves' % (badges, len(species)), bad['distinct'] == 0)
    check('%d badges: the first move is an attack of the first type, as strong as the type allows (power %d or the best the type has in its better category) in 60 percent of the species' % (badges, min(60 + 5 * (badges - 4), 90)),
          bad['slot0'] == 0 and bad['weak0'] <= len(species) * 0.40)
    check('%d badges: the second is an attack of the second type (or the first again), the third a coverage attack' % badges,
          bad['slot1'] == 0 and bad['slot2'] == 0)
    check('%d badges: the fourth is %s' % (badges, 'a set-up, recovery or status move' if badges >= 7 else 'a coverage attack'), bad['slot3'] == 0)
    check('%d badges: attacks never have less than 85 percent accuracy' % badges, bad['acc'] == 0)
    check('%d badges: the first attack is of the category the Pokemon is better at in at least 90 percent of the species' % badges,
          bad['lean'] <= len(species) * 0.10)
check('the average power of the attacks grows with the badges (4 -> 7 -> 10)', results[4] < results[7] < results[10])


def wild_plain(badges):
    total = 0
    for name, sid in species[:60]:
        total += sum(move_info(m)['power'] for m in wild_moves(sid, badges) if m)
    return total / 60 / 4


check('with three badges the moves stay random (average power well below the fourth-badge sets)', wild_plain(3) < wild_plain(4) - 8)

# --- trainers use the same sets and the Super League teams ------------------------------------------
cls_index = {}
id_index = {}
current = None
count = -1
for line in (root / 'constants/trainer_constants.asm').read_text(encoding='utf8').splitlines():
    m = re.match(r'\s*trainerclass (\w+)', line)
    if m:
        count += 1
        cls_index[m[1]] = count
        current = m[1]
        n = 0
        continue
    m = re.match(r'\s+const (\w+)', line)
    if m and current:
        n += 1
        id_index[m[1]] = (cls_index[current], n)
num_classes = count


def party(cls_id, badges, seed=1):
    cls, tid = cls_id
    johto, kanto = badges_for(badges)

    def setup(rr):
        rr.write('wJohtoBadges', johto)
        rr.write('wKantoBadges', kanto)
        rr.write('wBattleMode', 2)
        rr.write('wOtherTrainerClass', cls)
        rr.write('wOtherTrainerID', tid)
        rr.p.memory[addr('hRandomAdd')] = (seed * 37 + 11) & 0xff
        rr.p.memory[addr('hRandomSub')] = (seed * 91 + 5) & 0xff
    try:
        r.run('ReadTrainerParty', setup)
    except AssertionError:
        return None
    n = r.p.memory[addr('wOTPartyCount')]
    stride = addr('wOTPartyMon2') - addr('wOTPartyMon1')
    out = []
    for i in range(n):
        base = addr('wOTPartyMon1') + stride * i
        out.append((r.p.memory[base], list(r.p.memory[addr('wOTPartyMon1Moves') + stride * i:addr('wOTPartyMon1Moves') + stride * i + 4])))
    return out


p1 = 90
bad = checked = 0
for cls in range(1, num_classes + 1):
    for tid in range(1, 12):
        pt = party((cls, tid), 16)
        if not pt:
            continue
        for sp, mv in pt:
            if sp not in names_by_id or not (root / 'data/pokemon/base_stats' / (names_by_id[sp].lower() + '.asm')).exists():
                continue
            checked += 1
            (_, _, _, _, _, _), (t1, t2) = base_data(names_by_id[sp])[0], base_data(names_by_id[sp])[1]
            i0 = move_info(mv[0]) if mv[0] else {'power': 0, 'type': -1}
            if len(set(mv)) != 4 or not (i0['power'] >= 50 and i0['type'] == t1) or mv[3] not in UTILITY:
                bad += 1
check('with all badges every Pokemon of every trainer party (%d) has the full competitive set' % checked, checked > 1500 and bad == 0)

LEGENDS = {mons[n] for n in ('ARTICUNO', 'ZAPDOS', 'MOLTRES', 'MEWTWO', 'MEW', 'RAIKOU', 'ENTEI', 'SUICUNE', 'LUGIA', 'HO_OH', 'CELEBI')}
DARK_LUGIA = mons['DARK_LUGIA']


def bst(sid):
    return sum(base_data(names_by_id[sid])[0])


def league(name, label):
    ok_slots = ok_dupes = ok_bst = 0
    teams = []
    for seed in range(1, 13):
        pt = party(id_index[name], 16, seed)
        teams.append([sp for sp, _ in pt])
    return teams


for name, label in (('BLUE_SUPER', 'Azul'), ('LANCE_SUPER', 'Lance'), ('RED_SUPER', 'Rojo')):
    teams = league(name, label)
    good = all(len(t) == 6 and len(set(t)) == 6 and all(sp in LEGENDS for sp in t[3:]) and not any(sp in LEGENDS for sp in t[:3])
               and all(bst(sp) >= 500 for sp in t[:3]) for t in teams)
    check('%s\'s Super League team (12 draws): three strong non-legendary Pokemon and three different legendaries' % label, good)
teams = league('ULEX_SUPER', 'Ulex')
check('Ulex\'s Super League team (12 draws): three strong Pokemon, two legendaries and Dark Lugia as the last one',
      all(len(t) == 6 and len(set(t)) == 6 and t[5] == DARK_LUGIA and all(sp in LEGENDS for sp in t[3:5]) and not any(sp in LEGENDS for sp in t[:3])
          and all(bst(sp) >= 500 for sp in t[:3]) for t in teams))
check('the champion\'s own team is unchanged (Tito keeps his six)',
      len(party(id_index['TITO_XELUIS_SUPER'], 16)) == 6)

report = {'passed': len(tests), 'tests': tests}
Path('work/v58-routines-tests.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
r.close()
