"""Random-button fuzz in the overworld with a full bag/party (start menu, bag, party, summary, Pokegear, options...).
usage: menu_fuzz.py worker nworkers runs seed [presses]. Crash = boot screen / reset hook. Logs press sequence on crash."""
import json, random, sys
from lib import *
worker, nworkers, runs, seed = [int(a) for a in sys.argv[1:5]]
presses = int(sys.argv[5]) if len(sys.argv) > 5 else 1500
rng = random.Random(seed * 100 + worker)
BTN = ['a'] * 6 + ['b'] * 4 + ['up', 'down', 'left', 'right'] * 2 + ['start'] * 2 + ['select']
item_ids = [v for k, v in items.items() if v < 0xfa]
maplist = ['NEW_BARK_TOWN', 'ROUTE_29', 'GOLDENROD_CITY', 'VIOLET_POKECENTER_1F', 'ELMS_LAB', 'ROUTE_32']
import os
REPLAY = int(os.environ.get('REPLAY_RUN', '-1'))
for r in range(runs):
    faulthandler.dump_traceback_later(900, exit=True)
    if REPLAY >= 0 and r < REPLAY:      # burn the same random draws without emulating
        rng.choice(maplist); rng.choice([7, 12, 21]); ids_ = rng.sample(item_ids, 25)
        for _ in ids_: rng.randint(1, 99)
        for _ in range(presses): rng.choice(BTN); rng.choice([3, 8, 20]); rng.choice([2, 6])
        continue
    if REPLAY >= 0 and r > REPLAY:
        break
    m = rng.choice(maplist)
    g = G(m, *{'NEW_BARK_TOWN': (8, 9), 'ROUTE_29': (20, 6), 'GOLDENROD_CITY': (14, 20), 'VIOLET_POKECENTER_1F': (5, 5), 'ELMS_LAB': (4, 5), 'ROUTE_32': (10, 20)}[m], hour=rng.choice([7, 12, 21]))
    resets = []
    g.p.hook_register(0, 0x0100, lambda c: resets.append(1), None)
    g.party([150, 25, 133, 129, 251], level=40)
    g.write('wJohtoBadges', 0xff); g.write('wKantoBadges', 0xff)
    g.p.memory[g.a('wPlayerName'):g.a('wPlayerName') + 5] = [0x93, 0x88, 0x93, 0x8e, 0x50]
    for k in range(5):
        at = g.a('wPartyMonNicknames') + 11 * k
        g.p.memory[at:at + 11] = [0x8c, 0x84, 0x96, 0x93, 0x96, 0x8e, 0x50, 0, 0, 0, 0]
    ids = rng.sample(item_ids, 25)
    g.write('wNumItems', len(ids))
    arr = []
    for i in ids: arr += [i, rng.randint(1, 99)]
    g.p.memory[g.a('wItems'):g.a('wItems') + len(arr) + 1] = arr + [255]
    g.write('wNumBalls', 2); g.p.memory[g.a('wBalls'):g.a('wBalls') + 5] = [1, 5, 2, 5, 255]
    g.write('wNumKeyItems', 3); g.p.memory[g.a('wKeyItems'):g.a('wKeyItems') + 4] = [6, 7, 8, 255]
    g.p.memory[g.a('wStatusFlags')] |= 1       # dex
    g.p.memory[g.a('wPokegearFlags')] |= 0x1f
    g.p.tick(40)
    seq = []
    ring = []
    out = dict(run=r, worker=worker, map=m, seed=seed)
    for i in range(presses):
        b = rng.choice(BTN)
        seq.append(b)
        g.press(b, rng.choice([3, 8, 20]), hold=rng.choice([2, 6]))
        ring.append((i, b, ' | '.join(t for t in screen_text2(g) if t.strip())[:230]))
        del ring[:-14]
        if i % 10 == 0 and ('cartucho' in ' '.join(g.screen_text()) or resets):
            out['CRASH'] = i; out['seq_tail'] = seq[-60:]; out['ring'] = ring; open('logs/menufuzz_crash_w%d_r%d.txt' % (worker, r), 'w').write(' '.join(seq)); break
    if 'CRASH' not in out and (resets or crashed(g)):
        out['CRASH'] = presses; out['seq_tail'] = seq[-60:]
    out['final_map'] = where(g) if safe(g) else 'unsafe'
    g.close()
    print(json.dumps(out), flush=True)
