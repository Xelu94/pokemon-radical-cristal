"""REPRO: sprites of map B are wrong after crossing the A->B connection and become right after opening/closing the Start menu.
usage: py -3.12 -W ignore scripts/t_repro_menu.py ROUTE_38 ECRUTEAK_CITY 39 8 right"""
import sys; sys.path.insert(0, 'scripts')
from lib import *
alarm(300)
A, B, sx, sy, key = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
g = G(A, sx, sy); g.p.tick(60)
for _ in range(5):
    g.press(key, 16, hold=18)
g.p.tick(80)
print('after crossing  :', curmap(g), 'audit', audit(g))
shot(g, 'menu_before')
g.press('start', 30, hold=6); g.press('b', 40, hold=6); g.p.tick(60)
print('after Start,B   :', curmap(g), 'audit', audit(g))
shot(g, 'menu_after')
g.close()
