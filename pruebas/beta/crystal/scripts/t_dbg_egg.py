import sys
sys.path.insert(0, 'scripts')
from lib import *
g = G('GOLDENROD_CITY', 24, 8)
strong_party(g, level=30)
stride = g.a('wPartyMon2') - g.a('wPartyMon1')
g.write('wPartyCount', 2)
g.p.memory[g.a('wPartySpecies') + 1] = 253; g.p.memory[g.a('wPartySpecies') + 2] = 255
base = g.a('wPartyMon2'); g.p.memory[base:base + stride] = [0] * stride; g.p.memory[base] = 19
g.p.memory[g.a('wPartyMon1Level') + stride] = 1
g.p.memory[g.a('wPartyMon1Happiness') + stride] = 3
g.p.tick(60)
print('pos', g.pos())
for i in range(14):
    g.press('left' if i % 2 == 0 else 'right', 4, hold=16)
    print(i, g.pos(), 'counter', g.p.memory[g.a('wPartyMon1Happiness') + stride], 'steps', g.read('wStepCount'))
g.close()
