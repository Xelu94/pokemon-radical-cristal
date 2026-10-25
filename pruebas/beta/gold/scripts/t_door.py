from lib import *
g = G('AZALEA_GYM', 5, 14, hour=12)
strong_party(g)
g.p.tick(60)
print(where(g), g.pos())
g.press('down', 24, hold=16)
g.p.tick(150)
print(where(g), g.pos(), map_name_by_ids(*g.mem('wMapGroup',2)), maps.get('AZALEA_TOWN'), g.mem('wMapGroup',2))
g.close()
