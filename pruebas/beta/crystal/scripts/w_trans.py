"""Worker: walk through every warp of one map (both approach directions), re-entering, with sprite checks after each arrival.
argv: MAPSTEM"""
import sys, json, traceback
sys.path.insert(0, 'scripts')
from lib import *
import objs
alarm(560)
stem = sys.argv[1]
const = objs.const_of(stem)
pm = objs.parse_map(stem)
out = {'map': stem, 'tried': 0, 'moved': 0, 'issues': []}
for wi, w in enumerate(pm['warps']):
    dest = w['dest']
    if dest not in maps or w['dest'] == 'LAST_MAP' and False:
        continue
    for mode in ('down', 'up'):
        try:
            g = G(const, w['x'], w['y'] - 1 if mode == 'down' else w['y'] + 1)
            g.p.tick(60)
            out['tried'] += 1
            start = g.mem('wMapGroup', 2)
            wt = Watch(g, 'tr%s%d' % (stem, wi), shots=True)
            g.press('down' if mode == 'down' else 'up', 24, hold=16)
            g.p.tick(60)
            after = g.mem('wMapGroup', 2)
            if after == start:
                g.close(); continue
            out['moved'] += 1
            back = 'up' if mode == 'down' else 'down'
            for step, key in enumerate([None, back, mode]):
                if key:
                    g.press(key, 24, hold=16); g.p.tick(40)
                    if key == back and g.mem('wMapGroup', 2) != after and False:
                        pass
                for _ in range(8):
                    g.p.tick(12); wt.check('warp%d-%s-%d' % (wi, mode, step))
                if crashed(g):
                    out['issues'].append(('CRASH', stem, wi, mode, step)); break
            out['issues'] += [(i[0], i[1], i[2], i[3]) for i in wt.issues]
            g.close()
        except Exception as e:
            out['issues'].append(('ERR', repr(e)[:150]))
print('RESULT ' + json.dumps(out))
