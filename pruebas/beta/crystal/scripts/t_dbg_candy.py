import sys
sys.path.insert(0, 'scripts')
from lib import *
g = G('GOLDENROD_POKECENTER_1F', 6, 6)
g.party([1], level=5)
g.p.memory[g.a('wPartyMon1ID'):g.a('wPartyMon1ID') + 2] = g.p.memory[g.a('wPlayerID'):g.a('wPlayerID') + 2]
g.write('wJohtoBadges', 255); g.write('wKantoBadges', 255)
g.p.memory[g.a('wStatusFlags')] |= 1
g.write('wNumItems', 1); g.p.memory[g.a('wItems'):g.a('wItems') + 3] = [20, 99, 255]
g.p.tick(40)
imgs = []
def snap(): imgs.append(frame(g))
g.press('start', 30, hold=6)
for _ in range(8):
    if any('MOCHILA' in r and ('▶' in r) for r in decode_rows(g)): break
    g.press('down', 14, hold=6)
g.press('a', 50, hold=6); snap()
g.press('a', 30, hold=6); snap()
g.press('a', 40, hold=6); snap()
g.press('a', 50, hold=6); snap()
for _ in range(5): g.press('up', 8, hold=4)
snap()
g.press('a', 50, hold=6); snap()
g.press('a', 30, hold=6); snap()
g.press('a', 30, hold=6); snap()
print(sheet(imgs, 'dbg_candy', cols=4, scale=1))
g.close()
