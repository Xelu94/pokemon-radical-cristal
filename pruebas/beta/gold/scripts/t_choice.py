import sys
from lib import *
it = 0x5a
g = G('NEW_BARK_TOWN', 4, 2)
strong_party(g, moves=(106, 94))
g.p.memory[g.a('wPartyMon1Item')] = it
g.write('wNewBarkTownSceneID', 1)
g.p.tick(30); g.press('left', 20, hold=16)
for i in range(120):
    g.press('a', 25, hold=6)
    if battle_menu(g): print('menu at', i); break
print(screen_text2(g)[10:18])
g.press('up',4,hold=4); g.press('left',4,hold=4)
g.press('a', 30, hold=6)
print('after LUCHA', [r for r in screen_text2(g) if r.strip()])
for _ in range(3): g.press('up', 4, hold=4)
g.press('a', 30, hold=6)
print('after move1')
for i in range(80):
    if battle_menu(g): print('menu2 at', i); break
    g.press('a', 25, hold=6)
    if i % 6 == 0: print(i, (g.p.memory[0xff70]&7), g.read('wBattleMode'), ' '.join(t for t in screen_text2(g, range(12,18)) if t.strip('│┌└┐┘─ '))[:70])
print('item', g.read('wBattleMonItem'), 'choice', g.read('wPlayerChoiceMove'), 'enemy hp', g.p.memory[g.a('wEnemyMonHP')]*256+g.p.memory[g.a('wEnemyMonHP')+1])
g.press('up',4,hold=4); g.press('left',4,hold=4)
g.press('a', 30, hold=6)
for _ in range(3): g.press('up', 4, hold=4)
g.press('down', 4, hold=4)
print([r for r in screen_text2(g) if r.strip()])
g.press('a', 25, hold=6)
for i in range(30):
    print(i, [r for r in screen_text2(g, range(12,18)) if r.strip('│┌└┐┘─ ')])
    g.press('a', 25, hold=6)
    if crashed(g): print('CRASH'); break
g.close()
