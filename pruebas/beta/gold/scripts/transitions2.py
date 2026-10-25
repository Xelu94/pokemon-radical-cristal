"""Every building door / cave / stairs warp, both ways, with the oracles of lib.py (new-game state):
 at every arrival: check_objects (stale/missing/VRAM), mapobj_slots (walkers in table 2, objects without slot), then a Pack open/close
 (RefreshSprites) and the same checks again.  usage: transitions2.py worker nworkers"""
import json, sys
from lib import *
worker, nworkers = int(sys.argv[1]), int(sys.argv[2])
table = stem_to_const()
SKIP = ('ELEVATOR', 'LINK', 'TRADE', 'COLOSSEUM', 'TIME_CAPSULE', 'MOBILE', 'BATTLE_TOWER', 'PLAYERS_HOUSE_2F', 'COPYCATS_HOUSE_2F')
MOVE_WALKS = {2, 4, 5, 0xb, 0xc, 0xd, 0x13, 0x14}
jobs = []
seen = set()
for stem in sorted(table):
    const = table[stem]
    if const not in maps or any(k in const for k in SKIP): continue
    objs, bgs, warps = parse_map(stem)
    for (x, y, dest, n) in warps:
        if dest not in maps or any(k in dest for k in SKIP) or y < 1: continue
        if (const, x, y) in seen: continue
        seen.add((const, x, y)); jobs.append((const, x, y, dest))
jobs = jobs[worker::nworkers]
arm(3400)
def snap(g, label):
    mo = mapobj_slots(g)
    return dict(label=label, map=where(g)[0], problems=[p for p in check_objects(g) if p[0] != 'NOT_IN_LIST' or 'mapidx 255' not in p[1]],
                missing=[(o['idx'], o['sprite']) for o in mo if o['slot'] is None and o['type'] is not None],
                t2walk=[(o['idx'], o['sprite'], o['move']) for o in mo if o['slot'] is not None and o['slot'] >= 0x80 and o['type'] == 'WALKING' and o['move'] in MOVE_WALKS])
for const, x, y, dest in jobs:
    rec = dict(src=const, x=x, y=y, dest=dest, snaps=[])
    ok = False
    for dx, dy, key, back in ((0, -1, 'down', 'up'), (0, 1, 'up', 'down'), (-1, 0, 'right', 'left'), (1, 0, 'left', 'right')):
        if x + dx < 0 or y + dy < 0:
            continue
        try:
            g = G(const, x + dx, y + dy, hour=12)
            strong_party(g)
            g.p.tick(60)
            g.press(key, 24, hold=16)
            g.p.tick(60)
            if where(g)[0] == const:
                g.press(key, 24, hold=16)
            g.p.tick(150)
            if where(g)[0] != dest or where(g)[0] == const:
                g.close(); continue
            ok = True
            settle_ok(g)
            rec['snaps'].append(snap(g, 'in'))
            pack_cycle(g); rec['snaps'].append(snap(g, 'in+pack'))
            g.press(back, 24, hold=16)
            if where(g)[0] == dest: g.press(back, 24, hold=16)
            g.p.tick(150); settle_ok(g)
            rec['snaps'].append(snap(g, 'out'))
            pack_cycle(g); rec['snaps'].append(snap(g, 'out+pack'))
            if crashed(g): rec['CRASH'] = True
            g.close()
            break
        except Exception as e:
            rec['error'] = repr(e)[:200]
            try: g.close()
            except Exception: pass
            break
    if not ok:
        rec['nomove'] = True
        print(json.dumps(rec), flush=True); continue
    bad = [s for s in rec['snaps'] if s['problems'] or s['missing'] or s['t2walk']]
    if bad or rec.get('error') or rec.get('CRASH'):
        rec['bad'] = bad
        print(json.dumps(rec), flush=True)
print(json.dumps(dict(done=len(jobs), worker=worker)), flush=True)
