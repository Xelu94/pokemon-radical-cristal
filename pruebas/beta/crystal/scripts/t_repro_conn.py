"""REPRO: NPCs of map B drawn with wrong graphics after crossing the A->B map connection on foot, versus entering B by a warp.
usage: py -3.12 -W ignore scripts/t_repro_conn.py A B spawnx spawny key [extra_steps=2] [tag]
 e.g.  ROUTE_38 ECRUTEAK_CITY 39 8 right 2 ecruteak
Saves shots/conn_<tag>_walk.png and shots/conn_<tag>_warp.png (3x) and prints the audit of both."""
import sys; sys.path.insert(0, 'scripts')
from lib import *
alarm(300)
A, B, sx, sy, key = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
extra = int(sys.argv[6]) if len(sys.argv) > 6 else 2
tag = sys.argv[7] if len(sys.argv) > 7 else B.lower()
g = G(A, sx, sy); g.p.tick(60)
for _ in range(3 + extra):
    g.press(key, 16, hold=18)
g.p.tick(80)
print('WALK  map', curmap(g), 'pos', g.pos())
a1 = audit(g); print('  audit', a1, 'fullcheck', fullcheck(g))
im1 = shot(g, 'conn_%s_walk' % tag)
pos = g.pos(); g.close()
g2 = G(B, pos[0], pos[1]); g2.p.tick(100)
print('WARP  map', curmap(g2), 'pos', g2.pos())
print('  audit', audit(g2), 'fullcheck', fullcheck(g2))
im2 = shot(g2, 'conn_%s_warp' % tag)
g2.close()
print(im1, im2)
