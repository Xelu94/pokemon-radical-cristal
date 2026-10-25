"""REPRO visual: frames of the dude walking, cropped around his OAM sprites, for newbark vs warp entry.
usage: py -3.12 -W ignore scripts/t_repro_dude3.py newbark|warp ; writes shots/dude_walk_<mode>_g<gender>.png"""
import sys; sys.path.insert(0, 'scripts')
from lib import *
alarm(300)
frm = sys.argv[1]
g = G('NEW_BARK_TOWN', 0, 8) if frm == 'newbark' else G('ROUTE_29', 59, 8)
g.write('wRoute29SceneID', 1); g.party([152], level=6); g.p.tick(60)
g.p.button_press('left')
crops = []
last = None
for i in range(560):
    g.p.tick(1)
    if g.pos()[0] <= 52 and curmap(g) == 'ROUTE_29':
        g.p.button_release('left')
    if curmap(g) != 'ROUTE_29' or not settled(g):
        continue
    s = structs(g)[1]
    if s[0] != 0x23 or s[1] != 1:
        continue
    base = s[2]; lo = base & 0x7f if base >= 0x80 else base
    ents = [(y, x, t, a) for (idx, y, x, t, a) in oam_list(g) if ((a >> 3) & 1) == (1 if base < 0x80 else 0) and (lo <= t < lo + 12 or (base < 0x80 and lo + 0x80 <= t < lo + 0x80 + 12))]
    if not ents:
        continue
    x0 = min(e[1] for e in ents) - 8 - 6; y0 = min(e[0] for e in ents) - 16 - 6
    key = (tuple(sorted((e[2], e[3]) for e in ents)), x0, y0)
    if key == last:
        continue
    last = key
    im = frame(g)
    x0 = max(0, min(160 - 28, x0)); y0 = max(0, min(144 - 28, y0))
    crops.append(im.crop((x0, y0, x0 + 28, y0 + 28)).resize((112, 112), Image.NEAREST))
print(frm, 'distinct frames', len(crops))
cols = 12
rows = (len(crops) + cols - 1) // cols
sh = Image.new('RGB', (112 * cols, 112 * rows), (255, 255, 255))
for k, c in enumerate(crops):
    sh.paste(c, ((k % cols) * 112, (k // cols) * 112))
sh.save('shots/dude_walk_%s_g%s.png' % (frm, os.environ.get('PLAYER_GENDER', '0')))
g.close()
