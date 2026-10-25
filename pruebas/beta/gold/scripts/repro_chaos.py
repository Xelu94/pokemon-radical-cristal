"""Replay one chaos_battle record's spec (JSON line from logs/chaos_*.jsonl): usage repro_chaos.py <worker> <it> [menu-seed ...]"""
import json, random, sys
from lib import *
from read_jsonl import load
w, it = int(sys.argv[1]), int(sys.argv[2])
seeds = [int(a) for a in sys.argv[3:]] or [1]
rec = [r for r in load('logs/chaos_*.jsonl') if r['worker'] == w and r['it'] == it][0]
spec = rec['spec']
import os
for k in ('item','eitem','species','level','maxhp','hpfrac','ehp','emax'):
    if os.environ.get('SPEC_'+k.upper()) is not None: spec[k] = int(os.environ['SPEC_'+k.upper()])
print(spec)
for sd in seeds:
    rng = random.Random(sd)
    faulthandler.dump_traceback_later(300, exit=True)
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
    injected = False; crash = None; last = []
    for i in range(260):
        if rng.random() < 0.3 and injected and battle_menu(g):
            g.press('a', 20, hold=6)
            for _ in range(3): g.press('up', 4, hold=4)
            for _ in range(rng.randint(0, 3)): g.press('down', 4, hold=4)
        g.press('a', 22, hold=6)
        t = ' '.join(g.screen_text())
        if i % 5 == 0: last.append((i, t.strip()[-50:]))
        if 'cartucho' in t or resets:
            crash = i; break
        if not injected and (g.p.memory[0xff70] & 7) == 1 and g.read('wBattleMode') == 2 and g.read('wEnemyMonSpecies') and battle_menu(g):
            g.p.memory[g.a('wEnemyMonMoves'):g.a('wEnemyMonMoves') + 4] = spec['emoves']
            g.p.memory[g.a('wEnemyMonPP'):g.a('wEnemyMonPP') + 4] = [30] * 4
            g.p.memory[g.a('wEnemyMonItem')] = spec['eitem']
            e = spec['emax']; h = min(spec['ehp'], e)
            a = g.a('wEnemyMonMaxHP'); g.p.memory[a:a + 2] = [e >> 8, e & 255]
            a = g.a('wEnemyMonHP'); g.p.memory[a:a + 2] = [h >> 8, h & 255]
            injected = True
    print('seed', sd, 'crash at', crash, 'injected', injected, last[-4:] if crash is not None else '')
    if crash is not None:
        print('PC', hex(g.p.register_file.PC))
    g.close()
