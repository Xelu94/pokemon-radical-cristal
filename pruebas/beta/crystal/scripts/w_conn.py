"""Worker: cross every map connection (walk off the edge of map A into map B) and check B's NPC sprites.
In a connection crossing the game does NOT rebuild the sprite list (see MapSetupScript_Connection: no LoadMapGraphics),
so B's objects are drawn from A's list.   argv: MAPCONST_A [MAPCONST_B ...]  (default: all connections of A)
Reports NOSLOT (object sprite missing from the list => drawn with the player's graphics) and graphics mismatches.
"""
import sys, json, traceback
sys.path.insert(0, 'scripts')
from lib import *
alarm(560)
if os.environ.get('BASEROOT'):
    import lib as _lib
    from pathlib import Path as _P
    _lib.root = _P(os.environ['BASEROOT'])   # compare against another source tree / ROM (e.g. build/base0)

# --- parse attributes
attr = (root / 'data/maps/attributes.asm').read_text(encoding='utf8')
conns = {}      # const -> list of (dir, const_b, offset)
cur = None
for l in attr.splitlines():
    m = re.match(r'\s*map_attributes (\w+), (\w+),', l)
    if m:
        cur = m[2]; conns[cur] = []; continue
    m = re.match(r'\s*connection (north|south|west|east), (\w+), (\w+), (-?\d+)\s*$', l)
    if m and cur:
        conns[cur].append((m[1], m[3], int(m[4])))
size = {}
for l in (root / 'constants/map_constants.asm').read_text(encoding='utf8').splitlines():
    m = re.match(r'\s*map_const (\w+),\s*(\d+),\s*(\d+)', l)
    if m:
        size[m[1]] = (int(m[2]), int(m[3]))

A = sys.argv[1]
only_b = set(sys.argv[2:])
out = {'map': A, 'results': []}


def attempt(a, d, b, off):
    W, H = size[a][0] * 2, size[a][1] * 2
    if d in ('north', 'south'):
        cands = list(range(0, W, 1))
    else:
        cands = list(range(0, H, 1))
    # try a spread of candidates
    step = max(1, len(cands) // 12)
    cands = cands[::step] + cands[1::step]
    for c in cands:
        if d == 'north': sx, sy, key = c, 0, 'up'
        elif d == 'south': sx, sy, key = c, H - 1, 'down'
        elif d == 'west': sx, sy, key = 0, c, 'left'
        else: sx, sy, key = W - 1, c, 'right'
        g = None
        try:
            g = G(a, sx, sy)
            g.p.tick(50)
            if g.pos() != (sx, sy):
                g.close(); continue
            strong_party(g, level=100)
            for _ in range(3):
                g.press(key, 16, hold=18)
            g.p.tick(20)
            if curmap(g) != b:
                g.close(); continue
            wt = Watch(g, 'cn_%s_%s' % (a, b))
            res = {'from': a, 'dir': d, 'to': b, 'spawn': (sx, sy)}
            allp = []
            # let objects of B appear and be checked, walking a little further in
            for k in range(14):
                g.p.tick(20)
                if k in (4, 8):
                    g.press(key, 16, hold=18)
                    g.p.tick(20)
                if settled(g):
                    allp += audit(g)
                    allp += fullcheck(g)
                wt.check('conn')
            res['audit'] = [list(map(str, x)) for x in allp if str(x[2]) != '0xff'][:8]
            res['issues'] = [list(i) for i in wt.issues]
            res['list_has'] = len(used_sprites(g))
            # also the objects of B that have no struct yet: report their sprites vs the list
            slot = {sid for sid, t in used_sprites(g)}
            missing = []
            for k2, mo in enumerate(mapobjs(g), 1):
                if mo[1] and mo[1] not in slot:
                    missing.append((k2, sname(mo[1])))
            res['missing_from_list'] = missing
            g.close()
            return res
        except Exception as e:
            if g:
                try: g.close()
                except Exception: pass
            return {'from': a, 'dir': d, 'to': b, 'error': repr(e)[:150]}
    return {'from': a, 'dir': d, 'to': b, 'no_crossing': True}


for (d, b, off) in conns.get(A, []):
    if only_b and b not in only_b:
        continue
    out['results'].append(attempt(A, d, b, off))
print('RESULT ' + json.dumps(out))
