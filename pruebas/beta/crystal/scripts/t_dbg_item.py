import sys
sys.path.insert(0, 'scripts')
from lib import *
g = G('GOLDENROD_POKECENTER_1F', 6, 6)
strong_party(g, species=133, level=30, hp=200)
g.p.memory[g.a('wStatusFlags')] |= 1
g.write('wNumItems', 1); g.p.memory[g.a('wItems'):g.a('wItems') + 3] = [14, 3, 255]
g.p.tick(40)
imgs = []
def snap(): imgs.append(frame(g))
g.press('start', 30, hold=6); snap()
for _ in range(8):
    if any('MOCHILA' in r and ('▶' in r) for r in decode_rows(g)): break
    g.press('down', 14, hold=6)
snap()
g.press('a', 50, hold=6); snap()
print([r for r in decode_rows(g, range(0, 12))])
g.press('a', 30, hold=6); snap()
g.press('a', 40, hold=6); snap()
g.press('a', 40, hold=6); snap()
g.press('a', 40, hold=6); snap()
print(sheet(imgs, 'dbg_item', cols=4, scale=1))
g.close()
