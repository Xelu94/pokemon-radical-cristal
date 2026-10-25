import sys; sys.path.insert(0, 'scripts')
from lib import *
g = G('ROUTE_29', 55, 9); g.p.tick(100)
print('hour', g.p.memory[g.a('hHours')], 'tod', g.read('wTimeOfDay'), 'day', g.read('wCurDay'))
g.close()
