from lib import *
g = G('ROUTE_1', 4, 12)
strong_party(g)
print(g.p.memory[g.a('wPlayerID')], g.p.memory[g.a('wPlayerID')+1], g.mem('wPartyMon1ID', 2))
g.close()
