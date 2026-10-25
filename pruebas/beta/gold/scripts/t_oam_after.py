import sys
from lib import *
stem, ax, ay, key = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
table = stem_to_const()
g = G(table[stem], ax, ay, hour=12)
strong_party(g, moves=(94, 85, 89, 247))
g.p.tick(60)
g.press(key, 6, hold=14)
print('before', len(oam_check(g)))
g.press('a', 25, hold=6)
res, it = fight(g, max_iter=700)
print(res, it)
for i in range(40):
    g.press('a', 20, hold=6)
    if not script_running(g): break
g.p.tick(60)
print(where(g), 'oam bad', oam_check(g), 'objs', objs_in_view(g), check_objects(g))
shot(g, 'oam_after_%s' % stem)
for k in range(6):
    g.p.tick(20); print(len(oam_check(g)), end=' ')
print()
print('used', [(sprite_name(a), b) for a, b in used(g)])
g.close()
