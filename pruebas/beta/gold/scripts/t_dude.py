"""Route 29 tutorial dude: walk the player into the coord event and check OAM every few frames for distortion."""
from lib import *
arm(500)
g = G('ROUTE_29', 55, 9)
g.write('wRoute29SceneID', 1)
g.p.tick(60)
print('names', sprite_name(0x23), sprite_name(0x67), sprite_name(0xfb))
print('used', [(sprite_name(a), b) for a, b in used(g)])
print('check', check_objects(g))
print('t2walkers', table2_walkers(g))
bad_frames = 0
g.p.button_press('left')
for i in range(400):
    g.p.tick(2)
    if i == 40: g.p.button_release('left')
    b = oam_check(g)
    if b:
        bad_frames += 1
        if bad_frames < 5: print('frame', i, 'BAD OAM', b, 'pos', g.pos())
print('bad frames', bad_frames, 'pos', g.pos(), 'scene', g.read('wRoute29SceneID'))
shot(g, 'dude_end')
g.close()
