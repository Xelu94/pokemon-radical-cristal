import sys; sys.path.insert(0, 'scripts')
from lib import *
alarm(200)
name, x, y = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
g = G(name, x, y); g.p.tick(120)
print(fullcheck(g), audit(g))
g.close()
