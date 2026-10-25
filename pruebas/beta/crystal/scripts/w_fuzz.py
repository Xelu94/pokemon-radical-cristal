"""Worker: random-walk fuzz of one map. argv: mapname seed steps"""
import sys, random, json, traceback
sys.path.insert(0, 'scripts')
from lib import *
alarm(280)
name, seed, steps = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
ent = [c for c in catalog() if c[4] == name][0]
gi, num, x, y, name = ent
maps[name] = [gi, num]
rnd = random.Random(hash((name, seed)) & 0xffffffff)
out = {'map': name, 'seed': seed, 'issues': [], 'crash': False}
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
            out['issues'].append(('CRASH', curmap(g), [], shot(g, 'crash_%s_%d' % (name, seed))))
            break
        if settled(g):
            seen.add(curmap(g))
    out['maps_seen'] = sorted(seen)
    out['issues'] += [list(i) for i in w.issues]
    g.close()
except Exception as e:
    out['error'] = repr(e)[:200] + traceback.format_exc()[-300:]
print('RESULT ' + json.dumps(out, ensure_ascii=False))
