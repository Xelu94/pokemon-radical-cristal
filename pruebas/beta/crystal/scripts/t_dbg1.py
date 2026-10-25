import sys; sys.path.insert(0, 'scripts')
from lib import *
name=sys.argv[1]; x=int(sys.argv[2]); y=int(sys.argv[3])
g = G(name, x, y); g.p.tick(100)
print(curmap(g), 'vars', vars_(g))
print('\n'.join(listing(g)[:14]))
for i,b in enumerate(structs(g)):
    if b[0]: print(i, hex(b[0]), sname(b[0]), 'mapidx', b[1], 'tile', b[2], 'xy', b[0x10], b[0x11])
print('orph', oam_orphans(g))
print('oam', oam_list(g))
g.close()
