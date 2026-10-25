from lib import *
arm(300)
g = G('NEW_BARK_TOWN', 4, 2)
strong_party(g)
g.write('wNewBarkTownSceneID', 1)
g.p.tick(30); g.press('left', 20, hold=16)
for i in range(60):
    g.press('a', 25, hold=6)
    if g.read('wBattleMode') != 0:
        break
print('battle mode', g.read('wBattleMode'), 'svbk', g.p.memory[0xff70])
for i in range(40):
    g.p.tick(30)
    print(i, 'svbk', g.p.memory[0xff70] & 7, 'mode', g.read('wBattleMode'), 'enemy moves', g.mem('wEnemyMonMoves', 4), 'species', g.read('wEnemyMonSpecies'), 'txt', ' '.join(t for t in g.screen_text() if t)[:50])
    if i == 25: break
g.close()
