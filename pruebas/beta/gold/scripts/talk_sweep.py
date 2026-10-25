"""Talk to every object_event / bg_event of every map (default new-game state, strong party).
usage: talk_sweep.py <worker> <nworkers> [state] [stem-regex]       state: new (default) | late (all badges, many flags)
One JSON line per interaction: pages of text, end status (done / battle / hang / crash / nothing), sprite checks.
Approach: spawn on each of the four neighbour tiles of the target, face it, press A (first one that starts a script wins)."""
import json, re, sys, time
from lib import *

worker, nworkers = int(sys.argv[1]), int(sys.argv[2])
state = sys.argv[3] if len(sys.argv) > 3 else 'new'
only = re.compile(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4] != '-' else None
BATTLE_ONLY = len(sys.argv) > 5 and sys.argv[5] == 'battle'
table = stem_to_const()
stems = [s for s in sorted(table) if table[s] in maps]
if only:
    stems = [s for s in stems if only.search(s)]
SKIP = ('ELEVATOR', 'LINK', 'TRADE_CENTER', 'COLOSSEUM', 'TIME_CAPSULE', 'MOBILE', 'COPYCATS_HOUSE_2F', 'BATTLE_TOWER')
stems = [s for s in stems if not any(k in table[s] for k in SKIP)]
stems = stems[worker::nworkers]
DIRS = [('down', 0, 1, 'up'), ('up', 0, -1, 'down'), ('right', 1, 0, 'left'), ('left', -1, 0, 'right')]
# approach tile = target + (dx,dy) ; key = direction to press from there towards the target
APPROACH = [(0, 1, 'up'), (0, -1, 'down'), (-1, 0, 'right'), (1, 0, 'left')]
LATE_EVENTS = ['EVENT_BEAT_TITO_XELUIS'] if False else []


def late_state(g):
    g.write('wJohtoBadges', 0xff); g.write('wKantoBadges', 0xff)


def hour_for(o):
    tod = o.get('tod')
    if tod in (None, -1, 0, 7):
        return 12
    return 12 if tod & 2 else 7 if tod & 1 else 21


def interact(const, stem, o):
    res = dict(map=stem, kind=o['kind'], x=o['x'], y=o['y'], script=o.get('script'), sprite=o.get('sprite'), type=o.get('type'))
    h = hour_for(o) if o['kind'] == 'obj' else 12
    flag = o.get('flag') if o['kind'] == 'obj' else None
    clear = [flag] if flag and flag in EVENTS else []
    best = None
    for dx, dy, key in APPROACH:
        ax, ay = o['x'] + dx, o['y'] + dy
        if ax < 0 or ay < 0:
            continue
        faulthandler.dump_traceback_later(240, exit=True)
        g = None
        try:
            g = G(const, ax, ay, hour=h, clear=clear)
            strong_party(g)
            if state == 'late':
                late_state(g)
            g.p.tick(60)
            if where(g)[0] != const:
                g.close(); continue
            g.press(key, 6, hold=14)
            moved = g.pos() != (ax, ay)
            bag0 = g.bag()
            g.press('a', 25, hold=6)
            started = script_running(g) or g.read('wBattleMode') != 0
            if not started:
                g.p.tick(30)
                started = script_running(g)
            if not started:
                g.close(); continue
            pages, last, idle, status, steps, garbage = [], None, 0, 'done', 0, []
            for steps in range(70):
                if 'cartucho' in ' '.join(g.screen_text()):
                    status = 'CRASH'; break
                if (g.p.memory[0xff70] & 7) not in (0, 1):
                    g.p.tick(10); continue
                if g.read('wBattleMode') != 0:
                    status = 'battle'; break
                def grab():
                    box = screen_text2(g, range(12, 18))
                    if not (box[0].startswith('┌') and box[5].startswith('└')):
                        return []
                    body = [r.strip('│┌└┐┘─▼▲ ').strip() for r in box]
                    out = []
                    for b in body:
                        if b.strip('□ '):
                            if '□' in b:
                                garbage.append(b)
                            out.append(b)
                    return out
                prev, stable, ended = None, 0, 0
                cur = []
                for _ in range(40):
                    g.p.tick(8)
                    cur = grab()
                    if not script_running(g) and not cur:
                        ended += 1
                        if ended >= 3:
                            break
                    else:
                        ended = 0
                    if cur and cur == prev:
                        stable += 1
                    else:
                        stable = 0
                    prev = cur
                    if stable >= 3:
                        break
                if ended >= 3:
                    break
                if cur and cur != last:
                    pages.append(cur)
                    last = cur
                g.press('a', 6, hold=6)
            else:
                status = 'HANG'
            if status == 'done':
                for _ in range(40):
                    g.p.tick(8)
                    if (g.p.memory[0xff70] & 7) == 1 and g.read('wBattleMode') != 0:
                        status = 'battle'
                        break
                    if 'cartucho' in ' '.join(g.screen_text()):
                        status = 'CRASH'
                        break
            res.update(approach=key, status=status, steps=steps, pages=pages, moved=moved, ax=ax, ay=ay, garbage=sorted(set(garbage))[:5])
            if status == 'done':
                g.p.tick(30)
                res['bag_delta'] = {k: v - bag0.get(k, 0) for k, v in g.bag().items() if v != bag0.get(k, 0)}
                bad = oam_check(g) if safe(g) else []
                res['oam_bad'] = len(bad)
                res['sprite_problems'] = check_objects(g)[:3]
            g.close()
            return res
        except Exception as e:
            res['error'] = repr(e)[:160]
            try: g.close()
            except Exception: pass
    res.setdefault('status', 'no_script')
    return res


for stem in stems:
    const = table[stem]
    try:
        objs, bgs, warps = parse_map(stem)
    except Exception as e:
        print(json.dumps(dict(map=stem, error='parse ' + repr(e))), flush=True)
        continue
    mtext = (SRC / 'maps' / (stem + '.asm')).read_text(encoding='utf8')
    for o in objs + bgs:
        if o['kind'] == 'obj' and o['sprite'] in ('SPRITE_NONE',):
            continue
        if BATTLE_ONLY:
            if o['kind'] != 'obj':
                continue
            m = re.search(r'^' + re.escape(o['script']) + r':\n(.*?)(?=^\w+:\n)', mtext, re.M | re.S)
            body = m[1] if m else ''
            if o['type'] != 'OBJECTTYPE_TRAINER' and 'loadtrainer' not in body and 'startbattle' not in body and 'ULEX' not in o['script'].upper():
                continue
        r = interact(const, stem, o)
        print(json.dumps(r, ensure_ascii=False), flush=True)
