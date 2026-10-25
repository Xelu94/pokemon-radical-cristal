"""Worker: use a move in a wild battle, as the player or as the enemy; report crash / hang / odd result.
argv: mode(player|enemy) move_id [move_id ...]       env: WILD=1 is set here; PLAYER_GENDER inherited
The player side is a level-100 Mewtwo with 999 stats; the wild enemy gets all four move slots = the move under test.
"""
import sys, json, traceback, os
os.environ['WILD'] = '1'
sys.path.insert(0, 'scripts')
from lib import *
alarm(570)
mode = sys.argv[1]
ids = [int(a) for a in sys.argv[2:]]
MOVES = {}
n = -1
for l in (root / 'constants/move_constants.asm').read_text(encoding='utf8').splitlines():
    m = re.match(r'\s*const (\w+)', l)
    if m and not m[1].startswith('NUM_') and 'const_def' not in l:
        n += 1
        MOVES[n] = m[1]
res = {'mode': mode, 'moves': []}


def stat16(g, name, v):
    a = g.a(name)
    g.p.memory[a:a + 2] = [v >> 8, v & 255]


def battle_text(g):
    return ' '.join(r for r in decode_rows(g) if r)


def run(mv):
    item = {'id': mv, 'name': MOVES.get(mv, '?')}
    cat = [c for c in catalog() if c[4] == 'DARK_CAVE_VIOLET_ENTRANCE'][0]
    g = G('DARK_CAVE_VIOLET_ENTRANCE', cat[2], cat[3])   # cave: wild encounters on every step (WILD=1 patch)
    try:
        strong_party(g, level=100, moves=(150, 150, 150, 150) if mode == 'enemy' else (mv, mv, mv, mv))
        g.p.tick(30)
        fought = False
        for i in range(80):
            g.press(['left', 'right', 'up', 'down'][i % 4], 2, hold=14)
            if g.read('wBattleMode') in (1, 2):
                fought = True; break
        if not fought:
            item['error'] = 'no encounter'; return item
        # wait for the first menu
        menu = False
        for i in range(120):
            g.p.tick(20)
            if 'LUCHA' in battle_text(g):
                menu = True; break
            if crashed(g):
                item['crash'] = 'before menu'; return item
            g.press('a', 10, hold=4)
        if not menu:
            item['error'] = 'no battle menu'; item['text'] = battle_text(g)[:100]; return item
        used_seen = False
        texts = []
        for turn in range(3):
            if mode == 'enemy':
                a = g.a('wEnemyMonMoves'); g.p.memory[a:a + 4] = [mv, mv, mv, mv]
                a = g.a('wEnemyMonPP'); g.p.memory[a:a + 4] = [30, 30, 30, 30]
            else:
                a = g.a('wEnemyMonMoves'); g.p.memory[a:a + 4] = [150, 150, 150, 150]
            stat16(g, 'wEnemyMonHP', 999); stat16(g, 'wEnemyMonMaxHP', 999)
            if mode == 'enemy':
                stat16(g, 'wEnemyMonDefense', 999)
            # mash A: menu -> FIGHT -> move 1 -> text pages, until the menu is back (LUCHA in the menu rows)
            for k in range(70):
                g.press('a', 14, hold=4)
                g.p.tick(10)
                if crashed(g):
                    item['crash'] = 'turn %d press %d' % (turn, k); item['shot'] = shot(g, 'move_crash_%s_%d' % (mode, mv)); return item
                if g.read('wBattleMode') == 0:
                    break
                tb = ' / '.join(r[1:-1].strip() for r in decode_rows(g, range(13, 17)) if r[1:-1].strip())
                if tb and len(texts) < 24 and tb not in texts:
                    texts.append(tb[:100])
            if g.read('wBattleMode') == 0:
                break
        item['texts'] = texts[:14]
        item['ok'] = True
        return item
    except Exception as e:
        item['error'] = repr(e)[:200] + traceback.format_exc()[-200:]
        return item
    finally:
        g.close()


for mv in ids:
    res['moves'].append(run(mv))
print('RESULT ' + json.dumps(res, ensure_ascii=True))
