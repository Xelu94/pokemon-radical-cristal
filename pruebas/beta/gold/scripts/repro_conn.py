"""Visual repro of BUG-001: walk across a map connection, then refresh sprites (open/close the bag) and compare screenshots.
usage: repro_conn.py MAP x y key steps [extra_steps_key extra_steps]"""
from lib import *
arm(300)
name, x, y, key, n = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], int(sys.argv[5])
more = sys.argv[6:]
g = G(name, x, y, hour=12)
g.p.tick(60)
for i in range(n):
    g.press(key, 4, hold=16)
while more:
    k, c = more[0], int(more[1]); more = more[2:]
    for i in range(c): g.press(k, 4, hold=16)
g.p.tick(90)
print(where(g), objs_in_view(g), check_objects(g))
a = g.p.screen.image.convert('RGB').copy()
pack_cycle(g)
g.p.tick(30)
b = g.p.screen.image.convert('RGB').copy()
print(where(g), objs_in_view(g), check_objects(g))
s = Image.new('RGB', (320, 144)); s.paste(a, (0, 0)); s.paste(b, (160, 0))
s = s.resize((960, 432), Image.NEAREST)
out = 'shots/repro_conn_%s_%s_%s.png' % (name, x, y)
s.save(out); print(out)
g.close()
