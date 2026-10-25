"""Worker: evolution stones. For every EVOLVE_ITEM entry of data/pokemon/evos_attacks.asm use the item on the species and check the result.
argv: (none) -> all entries (about 20)   Uses Start -> MOCHILA -> first item -> USAR -> first mon; evolution screen is mashed through (B cancels are NOT pressed)."""
import sys, json, traceback
sys.path.insert(0, 'scripts')
from lib import *
alarm(580)
sp_ids = {}
n = 0
for l in open('work/source/constants/pokemon_constants.asm', encoding='utf8'):
    m = re.match(r'\s*const (\w+)\s*;\s*([0-9a-f]{2})', l)
    if m:
        sp_ids[m[1]] = int(m[2], 16)
t = open('work/source/data/pokemon/evos_attacks.asm', encoding='utf8').read()
blocks = re.split(r'\n(?=\w+EvosAttacks:)', t)
cases = []
for b in blocks:
    m = re.match(r'(\w+)EvosAttacks:', b)
    if not m:
        continue
    for e in re.findall(r'^\s*db EVOLVE_ITEM, (\w+), (\w+)', b, re.M):
        cases.append((m[1].upper(), e[0], e[1]))
res = {'cases': []}


def one(sp_name, item_name, want_name):
    out = {'species': sp_name, 'item': item_name, 'want': want_name}
    sp = sp_ids.get(sp_name)
    if sp is None:
        out['error'] = 'species const not found'; return out
    g = G('GOLDENROD_POKECENTER_1F', 6, 6)
    try:
        g.party([sp], level=40)
        g.p.memory[g.a('wPartyMon1ID'):g.a('wPartyMon1ID') + 2] = g.p.memory[g.a('wPlayerID'):g.a('wPlayerID') + 2]
        at = g.a('wPartyMonNicknames'); g.p.memory[at:at + 11] = [0x8c, 0x84, 0x96, 0x93, 0x96, 0x8e, 0x50, 0, 0, 0, 0]
        g.p.memory[g.a('wPlayerName'):g.a('wPlayerName') + 5] = [0x93, 0x88, 0x93, 0x8e, 0x50]
        g.p.memory[g.a('wStatusFlags')] |= 1
        g.write('wNumItems', 1); g.p.memory[g.a('wItems'):g.a('wItems') + 3] = [items[item_name], 5, 255]
        g.p.tick(40)
        g.press('start', 30, hold=6)
        for _ in range(8):
            if any('MOCHILA' in r and ('▶' in r) for r in decode_rows(g)):
                break
            g.press('down', 14, hold=6)
        g.press('a', 50, hold=6)
        # the stone may be in OTROS (4th) pocket: cycle right until the list shows an entry
        for _ in range(6):
            lst = decode_rows(g, range(1, 8))
            cur = [r for r in lst if ('▶' in r or '▷' in r)]
            if cur and 'SALIR' not in cur[0]:
                break
            g.press('right', 24, hold=6)
        g.press('a', 30, hold=6)
        g.press('a', 40, hold=6)
        g.press('a', 50, hold=6)
        for k in range(200):
            g.press('a', 18, hold=4)
            g.p.tick(10)
            if crashed(g):
                out['crash'] = 'press %d' % k; out['shot'] = shot(g, 'stone_crash_%s_%s' % (sp_name, item_name)); return out
        if settled(g):
            out['got'] = g.party_species()[0]
            out['ok'] = (out['got'] == sp_ids.get(want_name))
        return out
    except Exception as e:
        out['error'] = repr(e)[:150]
        return out
    finally:
        g.close()


for c in cases:
    res['cases'].append(one(*c))
print('RESULT ' + json.dumps(res, ensure_ascii=True))
