"""Route 29 'Ulex warning' dude (SPRITE_COOLTRAINER_M at (50,12), walks UP then RIGHT in Route29Tutorial1/2): how many OAM
samples show non-sprite tiles while he walks, depending on HOW the player arrived in Route 29 / time of day / player state.
Samples every 2 frames the whole way from spawn until the dialogue box opens. usage: dude_matrix.py [label ...]"""
import json, sys
from lib import *
arm(3000)

def run(label, mapname, x, y, keys, hour=12, weekday=None, state=None, pre=None, post_refresh=False):
    g = G(mapname, x, y, hour=hour, weekday=weekday)
    strong_party(g, species=152, level=6)
    g.write('wRoute29SceneID', 1); g.write('wNewBarkTownSceneID', 1)
    if state is not None: g.write('wPlayerState', state)
    g.p.tick(60)
    if pre: pre(g)
    bad = 0; first = None; samples = 0; slot = None; frames = []
    for key, n in keys:
        g.p.button_press(key)
        for i in range(n):
            g.p.tick(2)
            if safe(g):
                samples += 1
                b = oam_check(g)
                if b:
                    bad += 1
                    if first is None: first = (where(g), g.pos(), b[:2])
                if where(g)[0] == 'ROUTE_29':
                    s = [o for o in structs(g) if o['sprite'] == 0x23]
                    if s and slot is None: slot = s[0]['tile']
            if where(g)[0] == 'ROUTE_29' and g.pos()[0] <= 52 and key == 'left':
                break
        g.p.button_release(key)
    # let the scene run (dude walks, text) and keep sampling
    for i in range(300):
        g.p.tick(2)
        if safe(g):
            samples += 1
            b = oam_check(g)
            if b:
                bad += 1
                if first is None: first = (where(g), g.pos(), b[:2])
    res = dict(label=label, bad=bad, samples=samples, dude_tile=slot, first=first, end=where(g), scene=g.read('wRoute29SceneID'))
    g.close()
    print(json.dumps(res), flush=True)
    return res

L = lambda k, n: [(k, n)]
cases = {
 'newbark_connection': lambda: run('newbark_connection', 'NEW_BARK_TOWN', 2, 9, L('left', 400)),
 'direct': lambda: run('direct', 'ROUTE_29', 56, 9, L('left', 400)),
 'direct_row8': lambda: run('direct_row8', 'ROUTE_29', 56, 8, L('left', 400)),
 'route46_gate': lambda: run('route46_gate', 'ROUTE_29_ROUTE_46_GATE', 4, 6, [('down', 40), ('down', 20)] ),
 'cherrygrove_east': lambda: run('cherrygrove_east', 'CHERRYGROVE_CITY', 38, 6, L('right', 1400)),
 'newbark_bag_then_walk': lambda: run('newbark_bag', 'NEW_BARK_TOWN', 2, 9, L('left', 400), pre=lambda g: None),
 'bike_direct': lambda: run('bike_direct', 'ROUTE_29', 56, 9, L('left', 400), state=1),
 'bike_newbark': lambda: run('bike_newbark', 'NEW_BARK_TOWN', 2, 9, L('left', 400), state=1),
 'night_newbark': lambda: run('night_newbark', 'NEW_BARK_TOWN', 2, 9, L('left', 400), hour=21),
 'morn_newbark': lambda: run('morn_newbark', 'NEW_BARK_TOWN', 2, 9, L('left', 400), hour=7),
 'tuesday_newbark': lambda: run('tuesday_newbark', 'NEW_BARK_TOWN', 2, 9, L('left', 400), weekday=2, hour=12),
 'tuesday_direct': lambda: run('tuesday_direct', 'ROUTE_29', 56, 9, L('left', 400), weekday=2),
}
want = sys.argv[1:] or list(cases)
for k in want: cases[k]()
