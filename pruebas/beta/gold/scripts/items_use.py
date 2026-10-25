"""Use every item of the Items pocket (and Key Items) from the bag in the overworld with a 2-mon party; crash/hang detection.
usage: items_use.py worker nworkers [pocket: ITEM|KEY_ITEM]"""
import json, re, sys
from lib import *
worker, nworkers = int(sys.argv[1]), int(sys.argv[2])
pocket = sys.argv[3] if len(sys.argv) > 3 else 'ITEM'
names = []
for line in (SRC / 'data/items/names.asm').read_text(encoding='utf8').splitlines():
    m = re.match(r'\s*li "([^"]*)"', line)
    if m: names.append(m[1])
attrs = {}
cur = None
for line in (SRC / 'data/items/attributes.asm').read_text(encoding='utf8').splitlines():
    m = re.match(r'; (\w+)\s*$', line)
    if m: cur = m[1]
    m = re.match(r'\s*item_attribute (\S+), (\w+), (\S+), (\w+), (\w+), (\w+), (\w+)', line)
    if m and cur: attrs[cur] = dict(pocket=m[5], field=m[6], battle=m[7]); cur = None
todo = [(items[n], n, a) for n, a in attrs.items() if n in items and a['pocket'] == pocket and a['field'] != 'ITEMMENU_NOUSE']
todo.sort()
todo = todo[worker::nworkers]
arm(3300)
for iid, name, a in todo:
    rec = dict(id=iid, name=name, field=a['field'])
    faulthandler.dump_traceback_later(400, exit=True)
    try:
        g = G('ROUTE_29', 20, 6, hour=12)
        strong_party(g)
        g.party([150, 25], level=30)
        strong_party(g)
        g.p.memory[g.a('wPartyMon2HP'):g.a('wPartyMon2HP') + 2] = [0, 10]   # a hurt second mon so medicine has an effect
        if pocket == 'ITEM':
            g.write('wNumItems', 1); g.p.memory[g.a('wItems'):g.a('wItems') + 3] = [iid, 3, 255]
        else:
            g.write('wNumKeyItems', 1); g.p.memory[g.a('wKeyItems'):g.a('wKeyItems') + 2] = [iid, 255]
        g.p.tick(60)
        g.press('start', 30); g.press('down', 12); g.press('a', 50)   # MOCHILA
        if pocket == 'KEY_ITEM':
            for _ in range(5): g.press('right', 12)
        found = False
        for k in range(5):
            if any('×' in r for r in screen_text2(g, range(1, 12))) or pocket == 'KEY_ITEM':
                found = True; break
            g.press('right', 14)
        rec['found'] = found
        res = []
        g.press('a', 30)                       # item -> submenu
        t0 = ' | '.join(r for r in screen_text2(g) if r.strip())[:160]
        g.press('a', 30)                       # USAR
        crash = False
        for i in range(30):
            g.press('a', 25, hold=6)
            t = ' '.join(g.screen_text())
            if 'cartucho' in t: crash = True; rec['CRASH'] = 'press %d' % i; break
        for _ in range(5): g.press('b', 25)
        g.p.tick(60)
        rec['map'] = where(g); rec['menu0'] = t0
        rec['final'] = [r for r in screen_text2(g, range(12, 18)) if r.strip('│┌└┐┘─ ')][:3]
        if crashed(g): rec['CRASH'] = rec.get('CRASH', 'end')
        g.close()
    except Exception as e:
        rec['error'] = repr(e)[:200]
    print(json.dumps(rec, ensure_ascii=False), flush=True)
