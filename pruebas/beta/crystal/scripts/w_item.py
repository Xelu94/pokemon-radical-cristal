"""Worker: use bag items from the Start menu on the first party Pokemon; detect crash / hang; record outcomes.
argv: species level item_id [item_id ...]
The bag holds only that item (x3); Start -> MOCHILA -> find the pocket that shows it -> A -> A (first action) -> party mon -> mash A/B.
"""
import sys, json, traceback
sys.path.insert(0, 'scripts')
from lib import *
alarm(570)
species = int(sys.argv[1]); level = int(sys.argv[2]); ids = [int(a) for a in sys.argv[3:]]
att = open('work/source/data/items/attributes.asm', encoding='utf8').read()
names = {}
n = 0
for l in open('work/source/constants/item_constants.asm', encoding='utf8'):
    m = re.match(r'\s*const (\w+)\s*;\s*([0-9a-f]{2})\s*$', l)
    if m:
        names[int(m[2], 16)] = m[1]
pockets = re.findall(r'^\s*item_attribute [^,]+,[^,]+,[^,]+,[^,]+,\s*(\w+),', att, re.M)
res = {'species': species, 'level': level, 'items': []}


def texts_of(g):
    return [r for r in decode_rows(g) if r]


def box_text(g):
    return ' / '.join(r[1:-1].strip() for r in decode_rows(g, range(12, 18)) if r and r[1:-1].strip() and not r.startswith('+'))


def one(item_id):
    out = {'id': item_id, 'name': names.get(item_id, '?'), 'pocket': pockets[item_id - 1] if item_id <= len(pockets) else '?'}
    g = G('GOLDENROD_POKECENTER_1F', 6, 6)
    try:
        strong_party(g, species=species, level=level, hp=200)
        a = g.a('wPartyMon1HP'); g.p.memory[a:a + 2] = [0, 60]
        g.p.memory[g.a('wPartyMon1Status')] = 0x08 if item_id % 2 else 0   # poisoned on odd ids
        g.p.memory[g.a('wStatusFlags')] |= 1
        # legal bag placement
        pk = out['pocket']
        for sym in ('wNumItems', 'wNumBalls', 'wNumKeyItems'):
            g.write(sym, 0)
        for sym, lst in (('wItems', 'wItems'), ('wBalls', 'wBalls'), ('wKeyItems', 'wKeyItems')):
            g.p.memory[g.a(sym)] = 255
        for i_ in range(57):
            g.p.memory[g.a('wTMsHMs') + i_] = 0
        if pk == 'ITEM':
            g.write('wNumItems', 1); g.p.memory[g.a('wItems'):g.a('wItems') + 3] = [item_id, 3, 255]
        elif pk == 'BALL':
            g.write('wNumBalls', 1); g.p.memory[g.a('wBalls'):g.a('wBalls') + 3] = [item_id, 3, 255]
        elif pk == 'KEY_ITEM':
            g.write('wNumKeyItems', 1); g.p.memory[g.a('wKeyItems'):g.a('wKeyItems') + 2] = [item_id, 255]
        else:
            out['skip'] = pk; return out
        g.p.tick(40)
        g.press('start', 30, hold=6)
        for _ in range(8):
            if any('MOCHILA' in r and ('▶' in r) for r in decode_rows(g)):
                break
            g.press('down', 14, hold=6)
        g.press('a', 50, hold=6)
        # find the pocket that lists the item: cycle right up to 8 times until the list shows something other than empty
        shown = False
        for _ in range(8):
            rows = ' '.join(decode_rows(g))
            if '▶' in rows and any(c.isalpha() for c in rows.replace('MOCHILA', '')):
                # a selectable row exists when the list region contains x-quantity marker
                if 'x' in rows or '{f1}' in rows or True:
                    pass
            lst = decode_rows(g, range(1, 11))
            if any(('▶' in r or '▷' in r) for r in lst) and any(len(r.strip()) > 8 for r in lst):
                shown = True; break
            g.press('right', 24, hold=6)
        g.press('a', 30, hold=6)       # item submenu
        g.press('a', 40, hold=6)       # first action
        texts = []
        for k in range(50):
            g.press('a' if k % 4 != 3 else 'b', 18, hold=4)
            g.p.tick(16)
            if crashed(g):
                out['crash'] = 'press %d' % k; out['shot'] = shot(g, 'item_crash_%d_%d' % (species, item_id)); return out
            t = box_text(g)
            if t and t not in texts:
                texts.append(t[:80])
        out['texts'] = texts[-5:]
        if settled(g):
            out['party'] = g.party_species()
            out['hp'] = g.p.memory[g.a('wPartyMon1HP')] * 256 + g.p.memory[g.a('wPartyMon1HP') + 1]
            out['lvl'] = g.p.memory[g.a('wPartyMon1Level')]
        return out
    except Exception as e:
        out['error'] = repr(e)[:150]
        return out
    finally:
        g.close()


for i in ids:
    res['items'].append(one(i))
print('RESULT ' + json.dumps(res, ensure_ascii=True))
