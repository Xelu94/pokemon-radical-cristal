"""Fight every battle found by talk_sweep (status == 'battle').  usage: trainer_sweep.py worker nworkers [logs-glob]
For each: spawn on the approach tile, face, press A, play the pre-battle text, fight() with a level-100 Mewtwo (4 moves, 999 stats),
then read the post-battle script until idle.  Records: crash/hang, trainer class text, win/lose lines, rewards (money/bag),
sprite checks (check_objects/oam_check) after the battle, party deaths, event/scene state."""
import glob, json, sys
from lib import *
from read_jsonl import load

worker, nworkers = int(sys.argv[1]), int(sys.argv[2])
pattern = sys.argv[3] if len(sys.argv) > 3 else 'logs/talk_new_*.jsonl'
table = stem_to_const()
recs = [r for r in load(pattern) if r.get('status') == 'battle']
recs.sort(key=lambda r: (r['map'], r['x'], r['y']))
recs = recs[worker::nworkers]
KEYS = {'up': 'up', 'down': 'down', 'left': 'left', 'right': 'right'}


def money(g):
    a = g.a('wMoney')
    m = g.p.memory
    return m[a] * 65536 + m[a + 1] * 256 + m[a + 2]


def grab_box(g):
    box = screen_text2(g, range(12, 18))
    if not (box[0].startswith('┌') and box[5].startswith('└')):
        return []
    body = [r.strip('│┌└┐┘─▼▲ ').strip() for r in box]
    return [b for b in body if b.strip('□ ')]


def run(r):
    out = dict(map=r['map'], x=r['x'], y=r['y'], script=r.get('script'), sprite=r.get('sprite'), pre=r.get('pages'))
    const = table[r['map']]
    flag = None
    try:
        objs, bgs, _ = parse_map(r['map'])
        for o in objs:
            if o['x'] == r['x'] and o['y'] == r['y'] and o['script'] == r.get('script'):
                flag = o['flag']
    except Exception:
        pass
    faulthandler.dump_traceback_later(560, exit=True)
    g = G(const, r['ax'], r['ay'], hour=12, clear=[flag] if flag and flag in EVENTS else [])
    strong_party(g, moves=(94, 85, 89, 247))
    g.p.tick(60)
    key = r['approach']
    g.press(key, 6, hold=14)
    m0 = money(g); bag0 = g.bag()
    g.press('a', 25, hold=6)
    log = []
    res, it = fight(g, max_iter=700, log=log)
    out['fight'] = res; out['iters'] = it; out['moves_used'] = len(log)
    if res == 'end':
        # post-battle: read text until idle
        pages, last, idle = [], None, 0
        for i in range(60):
            g.p.tick(20)
            if 'cartucho' in ' '.join(g.screen_text()):
                out['post'] = 'CRASH'; break
            if not safe(g):
                continue
            cur = grab_box(g)
            if cur and cur != last:
                pages.append(cur); last = cur
            if not script_running(g):
                idle += 1
                if idle >= 3: break
            else:
                idle = 0
                g.press('a', 10, hold=6)
        else:
            out['post'] = 'HANG'
        out.setdefault('post', 'done')
        out['post_pages'] = pages
        g.p.tick(60)
        out['money_delta'] = money(g) - m0
        out['bag_delta'] = {k: v - bag0.get(k, 0) for k, v in g.bag().items() if v != bag0.get(k, 0)}
        out['sprite_problems'] = check_objects(g)[:3]
        out['oam_bad'] = len(oam_check(g)) if safe(g) else -1
        out['party_hp'] = [g.p.memory[g.a('wPartyMon1HP')] * 256 + g.p.memory[g.a('wPartyMon1HP') + 1]]
        out['map_after'] = where(g)
    g.close()
    return out


for r in recs:
    try:
        o = run(r)
    except Exception as e:
        o = dict(map=r['map'], x=r['x'], y=r['y'], error=repr(e)[:200])
    print(json.dumps(o, ensure_ascii=False), flush=True)
