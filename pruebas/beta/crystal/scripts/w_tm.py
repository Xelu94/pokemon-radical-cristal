"""Worker: use TM/HM items from the bag on party Pokemon (menu navigation by screen text), detect crash / hang.
argv: species tm_from tm_to [moves=4|1]     (tm numbers 1..57; 51-57 are HM01..07)
For every TM: Start -> MOCHILA -> TM pocket (left) -> select TM -> USAR -> party mon 1 -> mash A (and B at forget prompts); records the last texts.
"""
import sys, json, traceback
sys.path.insert(0, 'scripts')
from lib import *
alarm(570)
species = int(sys.argv[1]); a0, a1 = int(sys.argv[2]), int(sys.argv[3])
nmoves = int(sys.argv[4]) if len(sys.argv) > 4 else 4
res = {'species': species, 'nmoves': nmoves, 'tms': []}


def rows_text(g):
    return [r for r in decode_rows(g) if r]


def cursor_row(g, label):
    for r in decode_rows(g):
        if label in r and ('▶' in r or '▷' in r):
            return True
    return False


def goto(g, label, maxn=12):
    for _ in range(maxn):
        if cursor_row(g, label):
            return True
        g.press('down', 14, hold=6)
    return cursor_row(g, label)


def one(tm):
    item = {'tm': tm}
    g = G('GOLDENROD_POKECENTER_1F', 6, 6)
    try:
        strong_party(g, species=species, level=60)
        g.set_event('EVENT_GOT_A_POKEMON_FROM_ELM') if 'EVENT_GOT_A_POKEMON_FROM_ELM' in EVENTS else None
        g.p.memory[g.a('wStatusFlags')] |= 1   # pokedex
        # moves known
        base = g.a('wPartyMon1Moves')
        mv = [1, 2, 3, 4][:nmoves] + [0] * (4 - nmoves)
        g.p.memory[base:base + 4] = mv
        g.write('wNumItems', 0); g.p.memory[g.a('wItems'):g.a('wItems') + 1] = [255]
        for i in range(57):
            g.p.memory[g.a('wTMsHMs') + i] = 0
        g.p.memory[g.a('wTMsHMs') + tm - 1] = 1
        g.p.tick(40)
        g.press('start', 30, hold=6)
        if not goto(g, 'MOCHILA'):
            item['error'] = 'no MOCHILA entry: ' + ' | '.join(rows_text(g))[:100]; return item
        g.press('a', 40, hold=6)
        g.press('left', 30, hold=6)
        pocket = ' | '.join(rows_text(g))[:80]
        g.press('a', 30, hold=6)     # select TM
        g.press('a', 30, hold=6)     # USAR
        g.press('a', 40, hold=6)     # first party mon
        texts = []
        for k in range(60):
            g.press('a' if k % 5 != 4 else 'b', 20, hold=4)
            g.p.tick(20)
            if crashed(g):
                item['crash'] = 'press %d' % k
                item['shot'] = shot(g, 'tm_crash_%d_%d_%d' % (species, nmoves, tm))
                return item
            t = ' / '.join(r[1:-1].strip() for r in decode_rows(g, range(12, 18)) if r and r[1:-1].strip() and not r.startswith('+'))
            if t and t not in texts:
                texts.append(t[:90])
        item['texts'] = texts[-6:]
        return item
    except Exception as e:
        item['error'] = repr(e)[:150]
        return item
    finally:
        g.close()


for tm in range(a0, a1 + 1):
    res['tms'].append(one(tm))
print('RESULT ' + json.dumps(res, ensure_ascii=True))
