from lib import *
g = G('AZALEA_GYM', 3, 14, hour=12)
strong_party(g)
g.p.tick(60)
g.press('up', 6, hold=14)
g.press('a', 5, hold=6)
for i in range(14):
    g.p.tick(20)
    print('t', i, script_running(g), g.read('wScriptMode'), [r.strip('│┌└┐┘─▼▲ ') for r in screen_text2(g, range(12, 18)) if r.strip('│┌└┐┘─▼▲ ')])
    if i in (4, 6, 9): g.press('a', 6, hold=6); print('  pressed A')
for i in range(12):
    g.p.tick(10)
    print('post', i, script_running(g), g.read('wScriptMode'), g.read('wScriptRunning'))
g.close()
