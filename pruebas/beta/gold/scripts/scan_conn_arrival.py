"""For every connection: after crossing on foot, evaluate the NEW map's objects against the sprite list that is still the
OLD map's (no refresh happened).  Reports objects with no slot at all (drawn with the player's tiles), WALKING-type
sprites that sit in the standing-only second table while the object walks (movement type), and any sprite slot whose
VRAM content is not the right graphics.   usage: scan_conn_arrival.py worker nworkers"""
import json, re, sys
from lib import *
worker, nworkers = int(sys.argv[1]), int(sys.argv[2])
dims = {}
for line in (SRC / 'constants/map_constants.asm').read_text(encoding='utf8').splitlines():
    m = re.match(r'\s*map_const (\w+),\s*(\d+),\s*(\d+)', line)
    if m: dims[m[1]] = (int(m[2]), int(m[3]))
conns = []; cur = None
for line in (SRC / 'data/maps/attributes.asm').read_text(encoding='utf8').splitlines():
    m = re.match(r'\s*map_attributes (\w+), (\w+),', line)
    if m: cur = m[2]; continue
    m = re.match(r'\s*connection (\w+), (\w+), (\w+), (-?\d+)', line)
    if m and cur: conns.append((cur, m[1], m[3], int(m[4])))
conns = conns[worker::nworkers]
KEY = {'west': 'left', 'east': 'right', 'north': 'up', 'south': 'down'}
WALKERS = {2, 4, 5, 0xb, 0xc, 0xd, 0x13, 0x14}
arm(3400)
def spawn_for(a, d, k):
    w, h = dims[a]; W, H = 2 * w, 2 * h
    if d == 'west': return 2, k
    if d == 'east': return W - 3, k
    if d == 'north': return k, 2
    return k, H - 3
for a, d, b, off in conns:
    if a not in maps or b not in maps: continue
    w, h = dims[a]
    span = (2 * h) if d in ('west', 'east') else (2 * w)
    for k in sorted(set(range(1, span - 1, max(2, span // 10)))):
        x, y = spawn_for(a, d, k)
        rec = dict(a=a, dir=d, b=b, k=k)
        try:
            g = G(a, x, y, hour=12)
            g.p.tick(60)
            for i in range(9):
                g.press(KEY[d], 4, hold=16)
                if where(g)[0] == b: break
            if where(g)[0] != b:
                g.close(); continue
            g.p.tick(60)
            mo = mapobj_slots(g)
            rec['missing'] = [(o['idx'], o['sprite'], o['move']) for o in mo if o['slot'] is None and o['type'] is not None]
            rec['t2walk'] = [(o['idx'], o['sprite'], o['move'], o['slot']) for o in mo if o['slot'] is not None and o['slot'] >= 0x80 and o['type'] == 'WALKING' and o['move'] in WALKERS]
            rec['t2other'] = [(o['idx'], o['sprite'], o['move'], o['slot']) for o in mo if o['slot'] is not None and o['slot'] >= 0x80 and o['type'] == 'WALKING' and o['move'] not in WALKERS]
            rec['vram'] = [p for p in check_objects(g) if p[0] == 'VRAM_BAD']
            g.close()
            print(json.dumps(rec), flush=True)
            break
        except Exception as e:
            rec['error'] = repr(e)[:200]; print(json.dumps(rec), flush=True)
