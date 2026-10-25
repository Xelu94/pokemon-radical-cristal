from lib import *
arm(300)
g = G('CHERRYGROVE_CITY', 30, 4)
g.p.tick(60)
for h in (3, 6, 9, 10, 12, 17, 18, 22):
    set_clock(g, h, 4)
    g.p.tick(120)
    print('hour', h, 'hHours', g.p.memory[g.a('hHours')], 'tod', g.read('wTimeOfDay'), 'wday', g.read('wCurDay') % 7, flush=True)
g.close()
