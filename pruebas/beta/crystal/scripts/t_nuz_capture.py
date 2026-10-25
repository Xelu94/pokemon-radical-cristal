"""Nuzlocke capture rule: first wild encounter of a zone may be caught, the second may not; fleeing from the first uses it up.
usage: py -3.12 -W ignore scripts/t_nuz_capture.py [catch|flee]   Dark Cave Violet entrance (WILD=1: every step an encounter)
Prints every battle text and the party size after each battle."""
import sys, os
sys.path.insert(0, 'scripts')
os.environ['WILD'] = '1'
from lib import *
alarm(500)
mode = sys.argv[1] if len(sys.argv) > 1 else 'catch'
cat = [c for c in catalog() if c[4] == 'DARK_CAVE_VIOLET_ENTRANCE'][0]
g = G('DARK_CAVE_VIOLET_ENTRANCE', cat[2], cat[3])
strong_party(g, level=100, moves=(150, 150, 150, 150))
g.write('wNumBalls', 1); g.p.memory[g.a('wBalls'):g.a('wBalls') + 3] = [1, 99, 255]     # MASTER_BALL x99
g.write('wNumItems', 0); g.p.memory[g.a('wItems')] = 255
g.p.tick(40)


def to_battle():
    for i in range(80):
        g.press(['left', 'right', 'up', 'down'][i % 4], 2, hold=14)
        if g.read('wBattleMode') in (1, 2):
            return True
    return False


def box():
    return ' / '.join(r[1:-1].strip() for r in decode_rows(g, range(13, 17)) if r[1:-1].strip())


def wait_menu():
    for i in range(80):
        g.p.tick(15)
        if 'LUCHA' in ' '.join(decode_rows(g, range(12, 18))):
            return True
        g.press('a', 10, hold=4)
    return False


def log_until_end(n=60):
    seen = []
    for i in range(n):
        g.press('a', 20, hold=4)
        g.p.tick(10)
        t = box()
        if t and (not seen or seen[-1] != t):
            seen.append(t)
        if g.read('wBattleMode') == 0 and settled(g):
            break
    return seen


for b in range(1, 4):
    ok = to_battle()
    print('battle', b, 'started', ok, 'party before', g.party_species() if settled(g) else '?')
    if not ok:
        break
    if not wait_menu():
        print('  no menu', box()); break
    if mode == 'catch':
        # MOCHILA is below LUCHA
        g.press('down', 14, hold=5); g.press('a', 40, hold=5)
        for _ in range(4):
            g.press('right', 20, hold=5)
        print('   bag screen:', [r for r in decode_rows(g, range(0, 12)) if r][:5])
        g.press('a', 30, hold=5)        # item
        g.press('a', 60, hold=5)        # USAR
        texts = log_until_end()
    else:
        g.press('down', 14, hold=5); g.press('right', 14, hold=5); g.press('a', 40, hold=5)   # ESC
        texts = log_until_end()
    print('  texts:', texts[:10])
    g.p.tick(60)
    print('  after: party', g.party_species() if settled(g) else '?', 'battle', g.read('wBattleMode'))
g.close()
