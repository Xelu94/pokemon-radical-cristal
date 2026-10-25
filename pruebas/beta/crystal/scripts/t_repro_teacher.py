"""REPRO: Route 29 teacher (object 3, SPRITE_TEACHER) shows another NPC's graphics after a wild battle (or anything that reloads the map)
when Route 29 was entered on foot from New Bark Town. usage: py -3.12 -W ignore scripts/t_repro_teacher.py [newbark|warp]   (env FIXCONN=1, PLAYER_GENDER)"""
import sys, os
sys.path.insert(0, 'scripts')
os.environ['WILD'] = '1'
from lib import *
alarm(500)
mode = sys.argv[1] if len(sys.argv) > 1 else 'newbark'
g = G('NEW_BARK_TOWN', 0, 8) if mode == 'newbark' else G('ROUTE_29', 59, 8)
strong_party(g, level=50)
g.p.tick(60)
if mode == 'newbark':
    for _ in range(4):
        g.press('left', 16, hold=18)
g.p.tick(30)
for _ in range(3):
    g.press('down', 16, hold=18)
print('start', curmap(g), g.pos())
battles = 0
before = after = None
g.p.button_press('left')
for i in range(3000):
    g.p.tick(2)
    if g.read('wBattleMode') != 0:
        g.p.button_release('left')
        pre = [(b[0], b[1], b[2]) for b in structs(g) if b[0]]
        for _ in range(150):
            g.press('a', 20, hold=4)
            if g.read('wBattleMode') == 0 and settled(g):
                break
        g.p.tick(90)
        battles += 1
        sl = {s: t for s, t in used_sprites(g)}
        post = audit(g)
        print('battle', battles, 'at', g.pos(), 'audit after:', post)
        for b in structs(g):
            if b[0] and b[0] != 0x60:
                print('   object', sname(b[0]), 'mapidx', b[1], 'struct tile', b[2], 'list slot', sl.get(b[0]), '->', 'OK' if sl.get(b[0]) == b[2] else 'WRONG GRAPHICS (shows slot %s: %s)' % (b[2], [n.split()[1] for n in listing(g) if n.strip().split()[0] == str(b[2])]))
        shot(g, 'teacher_after_battle_%s_g%s' % (mode, os.environ.get('PLAYER_GENDER', '0')))
        if battles >= 2:
            break
        g.p.button_press('left')
    if g.pos()[0] <= 14:
        break
g.close()
