from lib import *
arm(300)
for init in (False, True):
    g = G('CHERRYGROVE_CITY', 30, 4, init=init)
    g.p.tick(60)
    print('init', init, 'vars', g.mem('wVariableSprites', 16), 'initialized', g.event('EVENT_INITIALIZED_EVENTS'))
    print(' objs', [(s['i'], sprite_name(s['sprite']), s['tile'], s['mapidx']) for s in structs(g) if s['sprite']])
    print(' hours', g.p.memory[g.a('hRTCHours')], g.read('wTimeOfDay'), 'startHour', g.read('wStartHour'))
    g.close()
g = G('CHERRYGROVE_CITY', 30, 4, hour=2, weekday=2)
g.p.tick(60)
print('tod', g.read('wTimeOfDay'), g.p.memory[g.a('hHours')], 'weekday', g.read('wCurDay') % 7)
g.close()
