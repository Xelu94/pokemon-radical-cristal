from lib import *
arm(200)
g = G('CHERRYGROVE_CITY', 30, 4)
g.p.tick(60)
print('vars', g.mem('wVariableSprites', 16), 'initialized', g.event('EVENT_INITIALIZED_EVENTS'))
print('used', [(sprite_name(a), b) for a, b in used(g)])
print('objs', [(s['i'], sprite_name(s['sprite']), s['tile'], s['mapidx']) for s in structs(g) if s['sprite']])
print('check', check_objects(g), table2_walkers(g))
g.close()
