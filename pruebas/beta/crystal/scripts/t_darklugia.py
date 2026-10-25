"""Dark Lugia (252): summary screen (front pic + cry text), Pokedex entry, and a wild battle with it as the player's lead (back pic).
usage: py -3.12 -W ignore scripts/t_darklugia.py ; screenshots shots/dl_*.png (girl/boy via PLAYER_GENDER)"""
import sys, os
sys.path.insert(0, 'scripts')
os.environ['WILD'] = '1'
from lib import *
alarm(500)
gd = os.environ.get('PLAYER_GENDER', '0')
cat = [c for c in catalog() if c[4] == 'DARK_CAVE_VIOLET_ENTRANCE'][0]
g = G('DARK_CAVE_VIOLET_ENTRANCE', cat[2], cat[3])
strong_party(g, species=252, level=100)
g.p.memory[g.a('wStatusFlags')] |= 1
g.p.memory[g.a('wPokedexCaught'):g.a('wPokedexCaught') + 32] = [0xff] * 32
g.p.memory[g.a('wPokedexSeen'):g.a('wPokedexSeen') + 32] = [0xff] * 32
g.p.tick(40)
# summary
g.press('start', 30, hold=6)
for k in range(8):
    rows = decode_rows(g)
    if any(('POK' in r and 'MON' in r and ('▶' in r)) for r in rows):
        break
    g.press('down', 14, hold=6)
print('menu:', [r for r in decode_rows(g) if r][:8])
g.press('a', 40, hold=6)          # party
g.press('a', 40, hold=6)          # first mon submenu
g.press('a', 60, hold=6)          # first option (summary?)
print('screen:', [r for r in decode_rows(g) if r][:6])
shot(g, 'dl_summary1_g%s' % gd)
for p in (2, 3):
    g.press('right', 40, hold=6)
    shot(g, 'dl_summary%d_g%s' % (p, gd))
for _ in range(6):
    g.press('b', 30, hold=6)
g.p.tick(60)
# battle
fought = False
for i in range(60):
    g.press(['left', 'right', 'up', 'down'][i % 4], 2, hold=14)
    if g.read('wBattleMode') in (1, 2):
        fought = True; break
print('battle', fought)
for i in range(14):
    g.press('a', 30, hold=6)
    shot(g, 'dl_battle%d_g%s' % (i, gd)) if i in (1, 3, 5, 8) else None
print('crash', crashed(g))
g.close()
