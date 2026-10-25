"""Visual repro (BUG-001/BUG-002 arrival variant): walk from map A across the connection into map B and take a screenshot
(bug); then spawn directly in B at the same tile and take another (control).
usage: repro_arrival.py A x y key B [extra_steps] [hour]"""
from lib import *
arm(300)
A, x, y, key, B = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
extra = int(sys.argv[6]) if len(sys.argv) > 6 else 3
hour = int(sys.argv[7]) if len(sys.argv) > 7 else 12
g = G(A, x, y, hour=hour)
strong_party(g)
g.p.tick(60)
for i in range(20):
    g.press(key, 4, hold=16)
    if where(g)[0] == B: break
for i in range(extra): g.press(key, 4, hold=16)
g.p.tick(90)
pos = g.pos(); w = where(g)
print('bug   ', w, objs_in_view(g), check_objects(g)[:4])
shot_a = g.p.screen.image.convert('RGB').copy()
g.close()
g = G(B, pos[0], pos[1], hour=hour)
strong_party(g)
g.p.tick(150)
print('control', where(g), objs_in_view(g), check_objects(g)[:4])
shot_b = g.p.screen.image.convert('RGB').copy()
g.close()
s = Image.new('RGB', (320, 144)); s.paste(shot_b, (0, 0)); s.paste(shot_a, (160, 0))
s = s.resize((960, 432), Image.NEAREST)
out = 'shots/ARRIVAL_%s_to_%s.png' % (A, B); s.save(out); print(out, '(left control, right bug)')
