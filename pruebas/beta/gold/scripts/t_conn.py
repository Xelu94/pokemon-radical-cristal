"""Cross a map connection then reload sprites (open/close start menu) and compare."""
from lib import *
arm(500)
name, x, y, key, n = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], int(sys.argv[5])
g = G(name, x, y)
g.p.tick(90)
def rep(label):
    m = where(g)
    print(label, m, 'used', len(used(g)), 'check', check_objects(g), 't2', table2_walkers(g), flush=True)
    return m
rep('spawn')
shot(g, 'conn_0')
for i in range(n):
    g.press(key, 4, hold=16)
    if i % 3 == 2: rep('step %d' % i)
g.p.tick(60)
rep('after-walk')
shot(g, 'conn_1')
print('objs', [(s['i'], sprite_name(s['sprite']), s['tile'], s['mapidx']) for s in structs(g) if s['sprite']])
print('used', [(sprite_name(a), b) for a, b in used(g)][:14])
g.reload_map()
g.p.tick(60)
rep('after-menu')
print('objs', [(s['i'], sprite_name(s['sprite']), s['tile'], s['mapidx']) for s in structs(g) if s['sprite']])
print('used', [(sprite_name(a), b) for a, b in used(g)][:14])
shot(g, 'conn_2')
g.close()
