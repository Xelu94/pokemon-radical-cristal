"""Save the game on Route 29 (after walking in from New Bark), soft-reset, CONTINUE, then audit the sprites and walk the dude scene.
usage: py -3.12 -W ignore scripts/t_savecontinue.py   (env PLAYER_GENDER)"""
import sys
sys.path.insert(0, 'scripts')
from lib import *
alarm(400)
g = G('NEW_BARK_TOWN', 0, 8)
strong_party(g, level=50)
g.p.tick(60)
for _ in range(2):
    g.press('left', 16, hold=18)
g.p.tick(40)
print('before save', curmap(g), g.pos(), 'audit', audit(g))
g.press('start', 30, hold=6)
txt = ' | '.join(r for r in decode_rows(g) if r)
print('menu:', txt[:150])
# find SAVE entry: navigate down until the cursor line contains GUARD
for k in range(8):
    rows = decode_rows(g)
    if any('GUARD' in r and r.strip().startswith(('▶', '▷')) or ('▶GUARD' in r.replace(' ', '')) for r in rows):
        break
    g.press('down', 12, hold=6)
g.press('a', 30, hold=6)
for _ in range(12):
    g.press('a', 40, hold=6)
    if 'guardado' in ' '.join(decode_rows(g)).lower() or 'GUARDADO' in ' '.join(decode_rows(g)):
        pass
g.p.tick(200)
print('after save text:', ' | '.join(r for r in decode_rows(g) if r)[:200])
# soft reset: A + B + START + SELECT
for b in ('a', 'b', 'start', 'select'):
    g.p.button_press(b)
g.p.tick(10)
for b in ('a', 'b', 'start', 'select'):
    g.p.button_release(b)
g.p.tick(400)
print('after reset:', ' | '.join(r for r in decode_rows(g) if r)[:200])
for _ in range(6):
    g.press('a', 90, hold=6)
g.p.tick(200)
print('after continue:', curmap(g), g.pos(), 'in overworld', settled(g))
print('audit', audit(g), 'fullcheck', fullcheck(g))
print('\n'.join(listing(g)[:4]))
g.close()
