"""Route 29 tutorial dude (COOLTRAINER_M, map object 1): walk the whole scene (he walks UP x4 then RIGHT x2) after arriving on Route 29 by
different paths. Every 2 frames: VRAM/ROM graphics of every object (fullcheck), object tile vs sprite list (audit), OAM ownership
(oam_orphans), and whether the dude's OAM ever uses walking-frame tiles (second half) while he moves.
usage: py -3.12 -W ignore scripts/t_dude_paths.py <path>      (env FIXCONN=1 tests the proposed fix; HOUR/DAYNUM; PLAYER_GENDER)
paths: newbark | cherrygrove | gate46 | warp | newbark_battle | newbark_menu | newbark_bike | newbark_surf
"""
import sys, json
sys.path.insert(0, 'scripts')
path = sys.argv[1]
import os
if path.endswith('battle'):
    os.environ['WILD'] = '1'
from lib import *
alarm(500)
OVERRIDES['write'] = [('wRoute29SceneID', 1)]
out = {'path': path, 'gender': os.environ.get('PLAYER_GENDER', '0'), 'fix': os.environ.get('FIXCONN', '0')}

if path.startswith('newbark'):
    g = G('NEW_BARK_TOWN', 0, 8); key, steps = 'left', 4
elif path == 'cherrygrove':
    g = G('CHERRYGROVE_CITY', 39, 6); key, steps = 'right', 4
elif path == 'gate46':
    g = G('ROUTE_29_ROUTE_46_GATE', 4, 2); key, steps = 'down', 0
else:
    g = G('ROUTE_29', 59, 8); key, steps = 'left', 0
g.write('wRoute29SceneID', 1)
strong_party(g, level=50)
g.p.tick(60)
for _ in range(steps):
    g.press(key, 16, hold=18)
g.p.tick(40)
if path == 'gate46':
    for _ in range(14):
        g.press('down', 16, hold=18)
        if curmap(g) == 'ROUTE_29':
            break
    g.p.tick(60)
out['arrived'] = curmap(g)
if path == 'newbark_menu':
    g.press('start', 30, hold=6); g.press('b', 30, hold=6); g.p.tick(60)
if path == 'newbark_bike':
    g.write('wPlayerState', 1)
    g.p.tick(10)
    g.press('start', 30, hold=6); g.press('b', 30, hold=6); g.p.tick(60)
if path == 'newbark_surf':
    g.write('wPlayerState', 4)
    g.p.tick(10)
    g.press('start', 30, hold=6); g.press('b', 30, hold=6); g.p.tick(60)
out['dude_slot_at_arrival'] = [t for s, t in used_sprites(g) if s == 0x23]

bad = {}
walk_tiles = set(); std_tiles = set()
battles = 0
going_west = g.pos()[0] > 53
g.p.button_press('left' if going_west else 'right')
for i in range(1500):
    g.p.tick(2)
    if g.read('wBattleMode') != 0:
        g.p.button_release('left'); g.p.button_release('right')
        battles += 1
        for _ in range(120):
            g.press('a', 20, hold=4)
            if g.read('wBattleMode') == 0 and settled(g):
                break
        g.p.tick(60)
        g.p.button_press('left' if going_west else 'right')
        continue
    if curmap(g) != 'ROUTE_29' or not settled(g):
        continue
    x = g.pos()[0]
    if (going_west and x <= 53) or ((not going_west) and x >= 53):
        g.p.button_release('left'); g.p.button_release('right')
    st = structs(g)
    dude = [b for b in st if b[0] == 0x23 and b[1] == 1]
    probs = [p for p in fullcheck(g) + audit(g) + oam_orphans(g) if str(p[2]) != '0xff' and str(p[1]) != '0xff']
    for p in probs:
        k = str(p)[:100]
        bad[k] = bad.get(k, 0) + 1
    if dude:
        base = dude[0][2]
        lo = base & 0x7f if base >= 0x80 else base
        bank = 1 if base < 0x80 else 0
        for (idx, y, xx, t, a) in oam_list(g):
            if ((a >> 3) & 1) != bank:
                continue
            if bank == 1 and lo + 0x80 <= t < lo + 0x80 + 12:
                walk_tiles.add(t)
            elif lo <= t < lo + 12:
                std_tiles.add(t)
    if g.event('EVENT_LEARNED_TO_CATCH_POKEMON'):
        # scene finished
        g.p.tick(120)
        break
out['battles'] = battles
out['dude_walk_frame_tiles'] = len(walk_tiles)
out['dude_standing_tiles'] = len(std_tiles)
out['problems'] = bad
out['scene_done'] = g.event('EVENT_LEARNED_TO_CATCH_POKEMON')
out['dude_struct_end'] = [b[:4] for b in structs(g) if b[0] == 0x23]
print('RESULT ' + json.dumps(out, ensure_ascii=True))
g.close()
