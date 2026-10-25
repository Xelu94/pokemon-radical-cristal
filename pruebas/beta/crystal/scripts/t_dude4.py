import sys; sys.path.insert(0, 'scripts')
from lib import *
alarm(300)
row = int(sys.argv[1]) if len(sys.argv) > 1 else 9
g = G('ROUTE_29', 55, row)
g.write('wRoute29SceneID', 1)
g.party([152], level=6)
g.p.tick(60)
g.p.button_press('left')
for i in range(200):
    g.p.tick(1)
    if i == 40: g.p.button_release('left')
    if i in (150, 165, 166, 170, 190):
        print(i, [(k, hex(b[0]), b[1], b[2], b[0x10], b[0x11]) for k, b in enumerate(structs(g)) if b[0]])
        print('  list', used_sprites(g)[:12])
        print('  oam', oam_list(g))
        print('  orphans', oam_orphans(g)[:4])
        print('  text', [t for t in g.screen_text() if t])
g.close()
