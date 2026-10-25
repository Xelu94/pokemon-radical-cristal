from lib import *
g = G('AZALEA_GYM', 3, 14, hour=12)
strong_party(g)
g.p.tick(60)
g.press('up', 6, hold=14)
g.press('a', 5, hold=6)
for i in range(30):
    g.p.tick(8)
    print(i, script_running(g), [r.strip('│┌└┐┘─▼▲ ') for r in screen_text2(g, range(12, 18)) if r.strip('│┌└┐┘─▼▲ ')])
g.close()
