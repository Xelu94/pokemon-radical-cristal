import sys; sys.path.insert(0, 'scripts')
from lib import *
alarm(300)
row = int(sys.argv[1]) if len(sys.argv) > 1 else 9
g = G('ROUTE_29', 55, row)
g.write('wRoute29SceneID', 1)
g.party([152], level=6)
g.p.tick(60)
g.p.button_press('left')
res = {}
for i in range(400):
    g.p.tick(1)
    if i == 40: g.p.button_release('left')
    for e in oam_orphans(g):
        res.setdefault((e[3], e[5]), []).append(i)
print({k: (len(v), v[:6]) for k, v in res.items()})
g.close()
