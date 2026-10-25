from lib import *
for h in (6, 12, 20):
    g = G('ROUTE_29', 27, 15, hour=h, weekday=2)
    g.p.tick(120)
    print(h, g.p.memory[g.a('hHours')], g.read('wTimeOfDay'), g.read('wCurDay') % 7, g.p.memory[g.a('hRTCHours')])
    g.close()
