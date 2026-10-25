"""Pokedex: open with everything seen/caught, scroll to the end of every sort mode, check the last entry and Dark Lugia (252).
usage: py -3.12 -W ignore scripts/t_dex.py"""
import sys
sys.path.insert(0, 'scripts')
from lib import *
alarm(500)
g = G('GOLDENROD_POKECENTER_1F', 6, 6)
strong_party(g, level=50)
g.p.memory[g.a('wStatusFlags')] |= 1
g.p.memory[g.a('wPokedexCaught'):g.a('wPokedexCaught') + 32] = [0xff] * 32
g.p.memory[g.a('wPokedexSeen'):g.a('wPokedexSeen') + 32] = [0xff] * 32
g.p.tick(40)
g.press('start', 30, hold=6)
g.press('a', 60, hold=6)       # POKeDEX is the first entry
print('dex main:', [r for r in decode_rows(g) if r][:10])
shot(g, 'dex_main')
for mode_i in range(4):
    # open the list for sort mode index mode_i: the dex "SELECT" cycles sort modes inside the list, A opens the entry
    for k in range(260):
        g.press('down', 3, hold=2)
        if crashed(g):
            print('CRASH scrolling'); break
    g.p.tick(30)
    rows = [r for r in decode_rows(g) if r]
    print('mode', mode_i, 'after 260 downs:', rows[:8])
    shot(g, 'dex_end_%d' % mode_i)
    g.press('a', 60, hold=6)
    rows = [r for r in decode_rows(g) if r]
    print('  entry:', rows[:6])
    shot(g, 'dex_entry_%d' % mode_i)
    g.press('b', 40, hold=6)
    g.press('select', 40, hold=6)    # next sort mode (if supported)
    for _ in range(3):
        g.press('up', 3, hold=2)
print('crashed', crashed(g))
g.close()
