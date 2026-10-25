"""REPRO: Route 29 tutorial dude distorted while walking when Route 29 is entered from New Bark Town on foot.
usage: py -3.12 -W ignore scripts/t_repro_dude.py [from=newbark|warp] [row=8]    (PLAYER_GENDER env: 0 boy, 1 girl)
 from=newbark : spawn at NEW_BARK_TOWN (0,8) and walk west across the map connection (sprite list built for New Bark)
 from=warp    : spawn directly in ROUTE_29 (sprite list built for Route 29) = control case
Prints the dude's tile slot, the VRAM check and saves frame sheets shots/repro_dude_<from>_*.png
"""
import sys; sys.path.insert(0, 'scripts')
from lib import *
alarm(300)
frm = sys.argv[1] if len(sys.argv) > 1 else 'newbark'
row = int(sys.argv[2]) if len(sys.argv) > 2 else 8
OVERRIDES['write'] = [('wRoute29SceneID', 1)]
if frm == 'newbark':
    g = G('NEW_BARK_TOWN', 0, row)
else:
    g = G('ROUTE_29', 59, row)
g.write('wRoute29SceneID', 1)
g.party([152], level=6)
g.p.tick(60)
print('start map', curmap(g), 'list size', len(used_sprites(g)))
# walk west until the dude reacts
frames = []
g.p.button_press('left')
dude_tile = None
for i in range(420):
    g.p.tick(2)
    if i % 2 == 0 and curmap(g) == 'ROUTE_29':
        s = structs(g)
        for k, b in enumerate(s):
            if b[0] == 0x23 and b[1] == 1:
                dude_tile = b[2]
    if i % 3 == 0:
        frames.append(frame(g))
    if g.pos()[0] <= 52 and curmap(g) == 'ROUTE_29':
        g.p.button_release('left')
print('map', curmap(g), 'pos', g.pos(), 'dude struct tile', dude_tile)
print('audit', audit(g), 'fullcheck', fullcheck(g))
print('\n'.join(listing(g)[:14]))
# pick frames where the dude is on screen
print(sheet(frames[-48:], 'repro_dude_%s_g%s' % (frm, os.environ.get('PLAYER_GENDER', '0')), cols=8, scale=1))
g.close()
