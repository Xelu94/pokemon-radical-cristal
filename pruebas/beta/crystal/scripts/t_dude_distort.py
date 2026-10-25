"""REPRO of the DISTORTION: Route 29 dude entered from New Bark Town on foot. While he walks, some frames use OAM tile numbers 156-159 in VRAM bank 0
(his 'up' frame tile 28-31 + $80 not masked) which address $89C0.. (BG/font tiles), i.e. garbage tiles. Saves shots/dude_distort_g<gender>.png.
usage: py -3.12 -W ignore scripts/t_dude_distort.py [newbark|warp]"""
import sys
sys.path.insert(0, 'scripts')
from lib import *
alarm(400)
mode = sys.argv[1] if len(sys.argv) > 1 else 'newbark'
OVERRIDES['write'] = [('wRoute29SceneID', 1)]
g = G('NEW_BARK_TOWN', 0, 8) if mode == 'newbark' else G('ROUTE_29', 59, 8)
g.write('wRoute29SceneID', 1); g.party([152], level=6); g.p.tick(60)
if mode == 'newbark':
    for _ in range(4):
        g.press('left', 16, hold=18)
g.p.tick(30)
g.p.button_press('left')
shots = []; log = []
prev = None
for i in range(900):
    g.p.tick(1)
    if g.pos()[0] <= 53 and curmap(g) == 'ROUTE_29':
        g.p.button_release('left')
    if curmap(g) != 'ROUTE_29' or not settled(g):
        continue
    orph = [o for o in oam_orphans(g) if o[3] >= 128 and ((o[4] >> 3) & 1) == 0]
    d = [b for b in structs(g) if b[0] == 0x23 and b[1] == 1]
    if orph and d:
        data = bytes(g.p.memory[0, 0x8000 + orph[0][3] * 16:0x8000 + orph[0][3] * 16 + 16]).hex()
        log.append((i, [(o[3], o[4]) for o in orph], d[0][8], d[0][9], data))
        if len(shots) < 8:
            ys = [o[1] for o in orph]; xs = [o[2] for o in orph]
            x0 = max(0, min(160 - 48, min(xs) - 14)); y0 = max(0, min(144 - 48, min(ys) - 24))
            shots.append(frame(g).crop((x0, y0, x0 + 48, y0 + 48)).resize((192, 192), Image.NEAREST))
    if g.event('EVENT_LEARNED_TO_CATCH_POKEMON'):
        break
print(mode, 'frames with garbage OAM tiles (bank 0, tile>=128):', len(log))
for l in log[:6]:
    print('  frame', l[0], 'oam(tile,attr)', l[1], 'dir', l[2], 'step', l[3], 'vram', l[4])
if shots:
    sh = Image.new('RGB', (192 * len(shots), 192), (255, 255, 255))
    for k, s_ in enumerate(shots):
        sh.paste(s_, (192 * k, 0))
    name = 'shots/dude_distort_%s_g%s.png' % (mode, os.environ.get('PLAYER_GENDER', '0'))
    sh.save(name); print('saved', name)
g.close()
