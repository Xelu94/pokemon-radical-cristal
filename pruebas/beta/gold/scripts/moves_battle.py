"""All-moves battle crash test.  usage: moves_battle.py <side:player|enemy> <worker> <nworkers> [first last]
side=player : the player's Mewtwo (stats 999) knows only move M and uses it on the New Bark ambush (CRISTAL's RATTATA).
side=enemy  : the player uses HARDEN each turn, the enemy RATTATA's four slots are all move M (written to WRAM at the
              first steady battle menu).
Crash = boot screen text ('cartucho') or a hit on the reset entry point.  Output: one JSON line per move."""
import json, sys, re
from lib import *

side, worker, nworkers = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
first = int(sys.argv[4]) if len(sys.argv) > 4 else 1
last = int(sys.argv[5]) if len(sys.argv) > 5 else 254
arm(3300)

names = {}
for i, line in enumerate((SRC / 'data/moves/names.asm').read_text(encoding='utf8').splitlines()):
    pass
mvnames = re.findall(r'li "([^"]+)"', (SRC / 'data/moves/names.asm').read_text(encoding='utf8'))


def one(m):
    rec = dict(move=m, name=mvnames[m - 1] if m - 1 < len(mvnames) else '?', side=side)
    g = G('NEW_BARK_TOWN', 4, 2)
    resets = []
    g.p.hook_register(0, 0x0100, lambda c: resets.append(1), None)
    strong_party(g)
    g.write('wNewBarkTownSceneID', 1)
    if side == 'player':
        g.p.memory[g.a('wPartyMon1Moves'):g.a('wPartyMon1Moves') + 4] = [m, 0, 0, 0]
        g.p.memory[g.a('wPartyMon1PP'):g.a('wPartyMon1PP') + 4] = [30, 0, 0, 0]
    else:
        g.p.memory[g.a('wPartyMon1Moves'):g.a('wPartyMon1Moves') + 4] = [106, 0, 0, 0]   # HARDEN
        g.p.memory[g.a('wPartyMon1PP'):g.a('wPartyMon1PP') + 4] = [30, 0, 0, 0]
    g.p.tick(30)
    g.press('left', 20, hold=16)
    injected = False
    log = []
    for i in range(300):
        g.press('a', 25, hold=6)
        t = ' '.join(g.screen_text())
        if 'cartucho' in t or resets:
            rec['CRASH'] = 'at press %d' % i
            break
        if side == 'enemy' and not injected and g.read('wBattleMode') == 2 and (g.p.memory[0xff70] & 7) == 1 and g.read('wEnemyMonSpecies'):
            g.p.memory[g.a('wEnemyMonMoves'):g.a('wEnemyMonMoves') + 4] = [m] * 4
            g.p.memory[g.a('wEnemyMonPP'):g.a('wEnemyMonPP') + 4] = [30] * 4
            injected = True
            rec['injected_at'] = i
        if i in (60, 120, 200):
            log.append(t.strip()[-60:])
        if g.read('wBattleMode') == 0 and (g.p.memory[0xff70] & 7) in (0, 1) and i > 40 and ('gan' in t or 'derrot' in t):
            rec['ended'] = 'at press %d' % i
            break
    rec['log'] = log
    rec['injected'] = injected
    g.close()
    return rec


for m in range(first, last + 1):
    if (m - first) % nworkers != worker:
        continue
    try:
        r = one(m)
    except Exception as e:
        r = dict(move=m, error=repr(e)[:200])
    print(json.dumps(r, ensure_ascii=False), flush=True)
