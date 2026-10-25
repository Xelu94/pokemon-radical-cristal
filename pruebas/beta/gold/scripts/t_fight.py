import sys, json
from lib import *
stem, x, y, ax, ay, key = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
table = stem_to_const()
g = G(table[stem], ax, ay, hour=12)
strong_party(g, moves=(94, 85, 89, 247))
g.p.tick(60)
g.press(key, 6, hold=14)
g.press('a', 25, hold=6)
log = []
res, it = fight(g, max_iter=int(sys.argv[7]) if len(sys.argv) > 7 else 700, log=log)
print(res, it, log[-6:])
print('\n'.join(screen_text2(g)))
print('enemy species', g.read('wEnemyMonSpecies'), 'hp', g.p.memory[g.a('wEnemyMonHP')]*256+g.p.memory[g.a('wEnemyMonHP')+1], 'moves', g.mem('wEnemyMonMoves', 4), 'mode', g.read('wBattleMode'), 'svbk', g.p.memory[0xff70])
print('player hp', g.p.memory[g.a('wBattleMonHP')]*256+g.p.memory[g.a('wBattleMonHP')+1], 'moves', g.mem('wBattleMonMoves',4))
shot(g, 'fight_debug')
g.close()
