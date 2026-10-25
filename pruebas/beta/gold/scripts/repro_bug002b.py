"""BUG-002 visual: strip of frames while the Route 29 dude walks to the player, arriving from New Bark (bug) vs spawning
directly in Route 29 (control)."""
from lib import *
arm(600)
def run(arrive_on_foot):
    if arrive_on_foot:
        g = G('NEW_BARK_TOWN', 2, 9, hour=12)
    else:
        g = G('ROUTE_29', 56, 9, hour=12)
    strong_party(g, species=152, level=6)
    g.write('wRoute29SceneID', 1); g.write('wNewBarkTownSceneID', 1)
    g.p.tick(60)
    frames = []
    g.p.button_press('left')
    for i in range(400):
        g.p.tick(2)
        if where(g)[0] == 'ROUTE_29' and g.pos()[0] <= 53:
            g.p.button_release('left')
            break
    for i in range(60):
        g.p.tick(3)
        frames.append(g.p.screen.image.convert('RGB').crop((0, 40, 160, 100)).copy())
    g.close()
    return frames
A = run(True); B = run(False)
W, H = 160, 60
rows = 12
s = Image.new('RGB', (W * 2, H * rows))
for r in range(rows):
    s.paste(B[r * 3], (0, r * H)); s.paste(A[r * 3], (W, r * H))
s = s.resize((s.width * 2, s.height * 2), Image.NEAREST)
s.save('shots/BUG002_walk_control_vs_bug.png'); print(s.size)
