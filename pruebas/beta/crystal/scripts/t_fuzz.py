"""Random-walk fuzzer over every map: spawn, strong party, random moves/A/B, battles auto-mashed, Watch checks sprite
consistency (VRAM vs ROM for each object, list vs struct tile, OAM ownership) and crash screen.
usage: py -3.12 -W ignore scripts/t_fuzz.py <seed> [steps=120] [procs=3] [first] [last]     (PLAYER_GENDER env respected)
Output: logs/fuzz_s<seed>_g<gender>.txt
"""
import sys, multiprocessing as mp, random, json, traceback
sys.path.insert(0, 'scripts')
from lib import *

SKIP = ('ELEVATOR', 'TRADE_CENTER', 'COLOSSEUM', 'TIME_CAPSULE', 'MOBILE', 'COPYCATS_HOUSE_2F', 'BATTLE_TOWER')


def one(args):
    entry, seed, steps = args
    gi, num, x, y, name = entry
    maps[name] = [gi, num]
    rnd = random.Random(hash((name, seed)) & 0xffffffff)
    out = {'map': name, 'seed': seed, 'issues': [], 'crash': False, 'maps_seen': []}
    try:
        g = G(name, x, y)
        strong_party(g, level=100)
        w = Watch(g, 'fz%d' % seed)
        g.p.tick(60)
        seen = set()
        for step in range(steps):
            r = rnd.random()
            if r < 0.7:
                d = rnd.choice(['up', 'down', 'left', 'right'])
                g.p.button_press(d)
                for _ in range(rnd.choice([1, 2, 3, 4])):
                    g.p.tick(8); w.check('walk')
                g.p.button_release(d)
            elif r < 0.9:
                press_watch(g, w, 'a', 1, 20)
            else:
                press_watch(g, w, 'b', 1, 20)
            if g.read('wBattleMode') != 0:
                for _ in range(60):
                    press_watch(g, w, 'a', 1, 20)
                    if g.read('wBattleMode') == 0 and settled(g):
                        break
            if crashed(g):
                out['crash'] = True
                out['issues'].append(('CRASH', curmap(g), shot(g, 'crash_%s_%d' % (name, seed))))
                break
            if settled(g):
                m = curmap(g)
                if m not in seen:
                    seen.add(m)
        out['maps_seen'] = sorted(seen)
        out['issues'] += [(t, m, p, path) for (t, m, p, path) in w.issues]
        g.close()
    except Exception as e:
        out['error'] = repr(e)[:200] + traceback.format_exc()[-300:]
    return out


if __name__ == '__main__':
    alarm(3500)
    seed = int(sys.argv[1])
    steps = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    procs = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    first = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    last = int(sys.argv[5]) if len(sys.argv) > 5 else 10 ** 6
    cat = [c for c in catalog() if not any(k in c[4] for k in SKIP)][first:last]
    gender = os.environ.get('PLAYER_GENDER', '0')
    f = open('logs/fuzz_s%d_g%s.txt' % (seed, gender), 'w')
    nbad = 0
    with mp.Pool(procs) as pool:
        for r in pool.imap_unordered(one, [(c, seed, steps) for c in cat], chunksize=2):
            if r['issues'] or 'error' in r:
                nbad += 1
                f.write(json.dumps(r, ensure_ascii=False) + '\n'); f.flush()
    print('maps', len(cat), 'with issues', nbad)
