import sys; sys.path.insert(0, 'scripts')
from lib import *
alarm(200)
name, x, y = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
g = G(name, x, y); g.p.tick(120)
print(name, 'gender', g.read('wPlayerGender'))
print('\n'.join(listing(g)))
for i, b in enumerate(structs(g)):
    if b[0]: print('struct', i, sname(b[0]), 'tile', b[2], 'mapidx', b[1], 'xy', b[16], b[17])
print('AUDIT', audit(g))
g.close()
