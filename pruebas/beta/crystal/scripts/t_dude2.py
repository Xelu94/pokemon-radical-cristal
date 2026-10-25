"""Route 29 dude: frame-by-frame OAM check while he walks toward the player."""
import sys; sys.path.insert(0, 'scripts')
from lib import *
alarm(300)
row = int(sys.argv[1]) if len(sys.argv) > 1 else 9
g = G('ROUTE_29', 55, row)
g.write('wRoute29SceneID', 1)
g.party([152], level=6)
g.p.tick(60)
g.p.button_press('left')
unknown = {}
for i in range(300):
    g.p.tick(1)
    if i == 40: g.p.button_release('left')
    u = oam_unknown(g)
    for e in u:
        unknown.setdefault(e[3], []).append(i)
print('unknown tiles by index', {k: (len(v), v[:5]) for k, v in unknown.items()})
g.close()
