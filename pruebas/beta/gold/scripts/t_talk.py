from lib import *
arm(200)
g = G('ROUTE_29', 27, 15, hour=12)
g.p.tick(60)
print(where(g), 'running', g.read('wScriptRunning'), 'mode', g.read('wScriptMode'))
g.press('down', 10, hold=16)
print(where(g), [(s['i'], sprite_name(s['sprite']), s['x'], s['y'], s['facing']) for s in structs(g) if s['sprite']])
g.press('a', 30, hold=6)
for i in range(8):
    print(i, 'running', g.read('wScriptRunning'), 'mode', g.read('wScriptMode'), text_box(g))
    g.press('a', 30, hold=6)
print('end running', g.read('wScriptRunning'))
g.close()
