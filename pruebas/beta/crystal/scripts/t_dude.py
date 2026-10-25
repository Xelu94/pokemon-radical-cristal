"""Route 29 tutorial dude (COOLTRAINER_M, object 1) walking toward the player: capture frames + OAM-vs-VRAM check.
usage: py -3.12 -W ignore scripts/t_dude.py [row=9] [tag]   (PLAYER_GENDER, NEWSTATE env respected)
"""
import sys; sys.path.insert(0, 'scripts')
from lib import *
alarm(300)
row = int(sys.argv[1]) if len(sys.argv) > 1 else 9
tag = sys.argv[2] if len(sys.argv) > 2 else 'dude'
g = G('ROUTE_29', 55, row)
g.write('wRoute29SceneID', 1)   # SCENE_ROUTE29_CATCH_TUTORIAL
g.party([152], level=6)
g.p.tick(60)
print('list', *listing(g)[:3], sep='\n ')
print('struct1', structs(g)[1][:4])
frames = []
crops = []
oam_bad = []

def oam_entries():
    # OAM at 0xfe00: y, x, tile, attr
    return [tuple(g.p.memory[0xfe00 + i * 4:0xfe00 + i * 4 + 4]) for i in range(40)]

def snap(tag_):
    st = structs(g)
    d = st[1]
    im = frame(g)
    sx, sy = d[0x17], d[0x18]
    crops.append(im.crop((max(0, sx - 8), max(0, sy - 8), max(0, sx - 8) + 32, max(0, sy - 8) + 32)).resize((96, 96), Image.NEAREST))
    frames.append(im)
    # dude's object tile and position
    tile = d[2]
    sx = d[0x17]; sy = d[0x18]
    ents = [e for e in oam_entries() if e[0] and abs((e[1] - 8) - (sx)) < 20 and abs((e[0] - 16) - sy) < 20]

g.p.button_press('left')
for i in range(60):
    g.p.tick(3)
    if i % 2 == 0:
        snap('w')
g.p.button_release('left')
for i in range(80):
    g.p.tick(3)
    if i % 2 == 0:
        snap('s')
cs = Image.new('RGB', (96 * 10, 96 * ((len(crops) + 9) // 10)))
for i, c in enumerate(crops):
    cs.paste(c, ((i % 10) * 96, (i // 10) * 96))
cs.save('shots/' + tag + '_crops.png')
print(sheet(frames[:40], tag + '_a', cols=10, scale=1))
print(sheet(frames[40:], tag + '_b', cols=10, scale=1))
print('fullcheck', fullcheck(g), 'audit', audit(g))
print(g.screen_text())
g.close()
