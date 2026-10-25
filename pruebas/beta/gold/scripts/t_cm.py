from lib import *
g = G('ROUTE_29', 27, 15, hour=12)
g.p.tick(60)
g.press('down', 10, hold=16); g.press('a', 30, hold=6)
for i in range(6):
    print(screen_text2(g, range(12, 18)))
    g.press('a', 30, hold=6)
g.close()
