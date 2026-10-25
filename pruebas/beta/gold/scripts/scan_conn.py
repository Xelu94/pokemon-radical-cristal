"""Cross every map connection (both directions) on foot, then force a sprite refresh (Pack open/close).
Usage: scan_conn.py <worker> <nworkers> [hour] > logs/conn_<worker>.jsonl
Hypothesis under test: MapSetupScript_Connection never calls RefreshSprites, so after crossing the object structs of the
new map were created against the OLD map's sprite list; the next RefreshSprites (any menu close, battle, ...) re-sorts the
list (AddOutdoorSprites now adds the current map's objects first) and the cached tiles go stale."""
import json, re, sys
from lib import *

worker, nworkers = int(sys.argv[1]), int(sys.argv[2])
hour = int(sys.argv[3]) if len(sys.argv) > 3 else 12
dims = {}
for line in (SRC / 'constants/map_constants.asm').read_text(encoding='utf8').splitlines():
    m = re.match(r'\s*map_const (\w+),\s*(\d+),\s*(\d+)', line)
    if m:
        dims[m[1]] = (int(m[2]), int(m[3]))
conns = []
cur = None
for line in (SRC / 'data/maps/attributes.asm').read_text(encoding='utf8').splitlines():
    m = re.match(r'\s*map_attributes (\w+), (\w+),', line)
    if m:
        cur = m[2]
        continue
    m = re.match(r'\s*connection (\w+), (\w+), (\w+), (-?\d+)', line)
    if m and cur:
        conns.append((cur, m[1], m[3], int(m[4])))
conns = conns[worker::nworkers]
KEY = {'west': 'left', 'east': 'right', 'north': 'up', 'south': 'down'}
arm(3400)


def spawn_for(a, d, k):
    w, h = dims[a]
    W, H = 2 * w, 2 * h
    if d == 'west': return 2, k
    if d == 'east': return W - 3, k
    if d == 'north': return k, 2
    return k, H - 3


for a, d, b, off in conns:
    if a not in maps or b not in maps:
        continue
    w, h = dims[a]
    span = (2 * h) if d in ('west', 'east') else (2 * w)
    samples = sorted(set(range(1, span - 1, max(2, span // 14))))
    done = 0
    for k in samples:
        if done >= 2:
            break
        x, y = spawn_for(a, d, k)
        rec = dict(a=a, dir=d, b=b, k=k)
        try:
            g = G(a, x, y, hour=hour)
            g.p.tick(60)
            for i in range(9):
                g.press(KEY[d], 4, hold=16)
                if where(g)[0] == b:
                    break
            if where(g)[0] != b:
                g.close()
                continue
            g.p.tick(90)
            rec['pos'] = where(g)[1]
            rec['objs'] = objs_in_view(g)
            rec['before'] = check_objects(g)
            rec['used_before'] = [(sprite_name(i), t) for i, t in used(g)]
            shot(g, 'conn_%s_%s_%s_a' % (a, d, b))
            pack_cycle(g)
            rec['after'] = check_objects(g)
            rec['objs_after'] = objs_in_view(g)
            rec['used_after'] = [(sprite_name(i), t) for i, t in used(g)]
            if rec['after'] or rec['objs'] != rec['objs_after']:
                shot(g, 'conn_%s_%s_%s_b' % (a, d, b))
            if crashed(g):
                rec['CRASH'] = True
            g.close()
            done += 1 if rec['objs'] else 0.5
        except Exception as e:
            rec['error'] = repr(e)[:200]
        print(json.dumps(rec), flush=True)
