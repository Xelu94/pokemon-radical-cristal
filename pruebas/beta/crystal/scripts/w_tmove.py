"""Worker: trainer battle (Route 30 Youngster Mikey) where the ENEMY mon is forced to know a given move set and all AI layers.
argv: move_ids_comma  enemy_hp  enemy_maxhp  [player_hp player_maxhp]
e.g. py -3.12 -W ignore scripts/w_tmove.py 179,175 1 200
"""
import sys, json, traceback, os
sys.path.insert(0, 'scripts')
from lib import *
alarm(300)
mv = [int(x) for x in sys.argv[1].split(',')]
while len(mv) < 4:
    mv.append(mv[0])
ehp, emax = int(sys.argv[2]), int(sys.argv[3])
php = int(sys.argv[4]) if len(sys.argv) > 4 else 999
pmax = int(sys.argv[5]) if len(sys.argv) > 5 else 999
out = {'moves': mv, 'ehp': ehp, 'emax': emax}


def s16(g, name, v):
    a = g.a(name); g.p.memory[a:a + 2] = [v >> 8, v & 255]


g = G('ROUTE_30', 5, 24)
try:
    pm = int(os.environ.get('PMOVE', '150'))
    strong_party(g, level=100, moves=(pm, pm, pm, pm), hp=999)
    s16(g, 'wPartyMon1HP', php); s16(g, 'wPartyMon1MaxHP', pmax)
    g.p.tick(40)
    g.press('up', 12, hold=6)
    for i in range(10):
        g.press('a', 20, hold=4)
        if g.read('wBattleMode') != 0:
            break
    # wait for battle mode 2 (trainer)
    for i in range(200):
        g.p.tick(10)
        if g.read('wBattleMode') == 2 or crashed(g):
            break
    out['battle_mode'] = g.read('wBattleMode')
    n = 0
    for turn in range(6):
        if g.read('wBattleMode') == 0:
            break
        a = g.a('wEnemyMonMoves'); g.p.memory[a:a + 4] = mv
        a = g.a('wEnemyMonPP'); g.p.memory[a:a + 4] = [30] * 4
        g.p.memory[g.a('wEnemyTrainerAIFlags'):g.a('wEnemyTrainerAIFlags') + 3] = [0xff, 0xff, 0xff]
        s16(g, 'wEnemyMonMaxHP', emax); s16(g, 'wEnemyMonHP', ehp)
        s16(g, 'wEnemyMonDefense', 999)
        for k in range(60):
            g.press('a', 14, hold=4)
            g.p.tick(8)
            if crashed(g):
                out['crash'] = 'turn %d press %d' % (turn, k); out['shot'] = shot(g, 'tmove_crash_%s_%d_%d' % ('_'.join(map(str, set(mv))), ehp, emax)); break
            if g.read('wBattleMode') == 0:
                break
        if out.get('crash'):
            break
    out['ok'] = 'crash' not in out
except Exception as e:
    out['error'] = repr(e)[:200] + traceback.format_exc()[-200:]
finally:
    g.close()
print('RESULT ' + json.dumps(out))
