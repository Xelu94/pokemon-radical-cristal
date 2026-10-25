"""Randomised battle fuzz: random player party member (species, level, HP/MaxHP, 4 random moves incl. FLAIL/REVERSAL, random held item),
the enemy of the New Bark ambush gets random moves/HP/item (written at the first steady battle menu), 40 turns of random move choices.
usage: chaos_battle.py worker nworkers n seed.   Output: one JSON line per iteration; CRASH flagged."""
import json, random, sys
from lib import *
worker, nworkers, n, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
rng = random.Random(seed * 1000 + worker)
item_ids = sorted(v for k, v in items.items())
import os
PLAYER_IDS = [i for i in item_ids if i not in (0x2d, 0x32, 0x5a)] if os.environ.get('NO_CHOICE') else item_ids
for it in range(n):
    spec = dict(
        species=rng.randint(1, 251), level=rng.choice([5, 20, 50, 100]),
        hpfrac=rng.choice([1, 5, 20, 50, 100]), maxhp=rng.choice([30, 150, 255, 256, 300, 600, 999]),
        moves=[rng.choice([175, 179, 175, 179] + list(range(1, 255))) for _ in range(4)],
        item=rng.choice([0, 0] + PLAYER_IDS), eitem=rng.choice([0, 0] + item_ids),
        emoves=[rng.choice([175, 179] + list(range(1, 255))) for _ in range(4)],
        ehp=rng.choice([1, 3, 10, 50, 100]), emax=rng.choice([20, 100, 255, 256, 300]),
    )
    rec = dict(it=it, worker=worker, seed=seed, spec=spec)
    faulthandler.dump_traceback_later(500, exit=True)
    try:
        g = G('NEW_BARK_TOWN', 4, 2)
        resets = []
        g.p.hook_register(0, 0x0100, lambda c: resets.append(1), None)
        strong_party(g, species=spec['species'], level=spec['level'])
        mx = spec['maxhp']; hp = max(1, mx * spec['hpfrac'] // 100)
        a = g.a('wPartyMon1MaxHP'); g.p.memory[a:a + 2] = [mx >> 8, mx & 255]
        a = g.a('wPartyMon1HP'); g.p.memory[a:a + 2] = [hp >> 8, hp & 255]
        g.p.memory[g.a('wPartyMon1Moves'):g.a('wPartyMon1Moves') + 4] = spec['moves']
        g.p.memory[g.a('wPartyMon1PP'):g.a('wPartyMon1PP') + 4] = [30] * 4
        g.p.memory[g.a('wPartyMon1Item')] = spec['item']
        g.write('wNewBarkTownSceneID', 1)
        g.p.tick(30); g.press('left', 20, hold=16)
        injected = False
        t_prev = ''
        for i in range(260):
            if rng.random() < 0.3 and injected and battle_menu(g):
                g.press('a', 20, hold=6)
                for _ in range(3): g.press('up', 4, hold=4)
                for _ in range(rng.randint(0, 3)): g.press('down', 4, hold=4)
            g.press('a', 22, hold=6)
            t = ' '.join(g.screen_text())
            if 'cartucho' in t or resets:
                rec['CRASH'] = 'at press %d' % i; break
            if not injected and (g.p.memory[0xff70] & 7) == 1 and g.read('wBattleMode') == 2 and g.read('wEnemyMonSpecies') and battle_menu(g):
                g.p.memory[g.a('wEnemyMonMoves'):g.a('wEnemyMonMoves') + 4] = spec['emoves']
                g.p.memory[g.a('wEnemyMonPP'):g.a('wEnemyMonPP') + 4] = [30] * 4
                g.p.memory[g.a('wEnemyMonItem')] = spec['eitem']
                e = spec['emax']; h = min(spec['ehp'], e)
                a = g.a('wEnemyMonMaxHP'); g.p.memory[a:a + 2] = [e >> 8, e & 255]
                a = g.a('wEnemyMonHP'); g.p.memory[a:a + 2] = [h >> 8, h & 255]
                injected = True; rec['injected'] = i
            if injected and g.read('wBattleMode') == 0 and (g.p.memory[0xff70] & 7) in (0, 1) and i > 30:
                rec['ended'] = i; break
        g.close()
    except Exception as e:
        rec['error'] = repr(e)[:200]
    print(json.dumps(rec), flush=True)
