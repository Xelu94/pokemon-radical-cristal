"""BUG-002 repro: Route 29 tutorial dude distorted while he walks, when the player ARRIVES from New Bark Town on foot
(connection crossing keeps New Bark's sprite arrangement, where COOLTRAINER_M is in the standing-only second table).
Sets wRoute29SceneID like a fresh game (scene 1 = catch tutorial) and samples OAM every 2 frames."""
from lib import *
arm(600)
from_where = sys.argv[1] if len(sys.argv) > 1 else 'newbark'
g = G('NEW_BARK_TOWN', 2, 9, hour=12)
strong_party(g, species=152, level=6)
g.write('wRoute29SceneID', 1); g.write('wNewBarkTownSceneID', 1)
g.p.tick(60)
print('start', where(g), [(sprite_name(i), t) for i, t in used(g)][:14])
frames = []
bad = 0
g.p.button_press('left')
for i in range(400):
    g.p.tick(2)
    if i % 4 == 0:
        if not safe(g): continue
        b = oam_check(g)
        if b:
            bad += 1
            if bad <= 3: print('t', i, 'BAD OAM', len(b), where(g), b[:4])
        if where(g)[0] == 'ROUTE_29' and g.pos()[0] <= 55:
            frames.append(g.p.screen.image.convert('RGB').copy())
    if where(g)[0] == 'ROUTE_29' and g.pos()[0] <= 52:
        g.p.button_release('left')
print('bad samples', bad, where(g), 'dude struct:', [(s['i'], sprite_name(s['sprite']), s['tile'], s['facing']) for s in structs(g) if s['sprite']])
print('used', [(sprite_name(i), t) for i, t in used(g)][:14])
for i in range(12):
    g.p.tick(6)
    frames.append(g.p.screen.image.convert('RGB').copy())
    b = oam_check(g) if safe(g) else []
    if b: print('later BAD OAM', len(b), b[:3])
sel = frames[-30:]
W = 160
s = Image.new('RGB', (W * 6, 144 * ((len(sel) + 5) // 6)))
for k, im in enumerate(sel): s.paste(im, ((k % 6) * W, (k // 6) * 144))
s.save('shots/BUG002_%s.png' % from_where)
g.close()
