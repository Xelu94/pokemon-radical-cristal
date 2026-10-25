"""Worker: Rare Candy quantity selector on many species (level-ups, random move offers, evolution), detect crash/hang.
argv: level badges_byte qty_ups species [species ...]
Start -> MOCHILA -> MEDICINA first item (RARE_CANDY) -> A -> USAR -> mon -> quantity (up x qty_ups) -> A -> mash (A, with B at move-forget prompts).
Reports final level / species / crash."""
import sys, json, traceback
sys.path.insert(0, 'scripts')
from lib import *
alarm(580)
level, badges, ups = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
species_list = [int(a) for a in sys.argv[4:]]
RARE = items['RARE_CANDY']
res = {'level': level, 'badges': badges, 'ups': ups, 'mons': []}


def one(sp):
    item = {'sp': sp}
    g = G('GOLDENROD_POKECENTER_1F', 6, 6)
    try:
        g.party([sp], level=level)
        g.p.memory[g.a('wPartyMon1ID'):g.a('wPartyMon1ID') + 2] = g.p.memory[g.a('wPlayerID'):g.a('wPlayerID') + 2]
        exp = int(level ** 3)
        g.p.memory[g.a('wPartyMon1Exp'):g.a('wPartyMon1Exp') + 3] = [exp >> 16, (exp >> 8) & 255, exp & 255]
        at = g.a('wPartyMonNicknames'); g.p.memory[at:at + 11] = [0x8c, 0x84, 0x96, 0x93, 0x96, 0x8e, 0x50, 0, 0, 0, 0]
        g.write('wJohtoBadges', badges); g.write('wKantoBadges', badges)
        g.p.memory[g.a('wPlayerName'):g.a('wPlayerName') + 5] = [0x93, 0x88, 0x93, 0x8e, 0x50]
        g.p.memory[g.a('wStatusFlags')] |= 1
        g.write('wNumItems', 1); g.p.memory[g.a('wItems'):g.a('wItems') + 3] = [RARE, 99, 255]
        g.p.tick(40)
        g.press('start', 30, hold=6)
        for _ in range(8):
            if any('MOCHILA' in r and ('▶' in r) for r in decode_rows(g)):
                break
            g.press('down', 14, hold=6)
        g.press('a', 50, hold=6)
        g.press('a', 30, hold=6)      # select item
        g.press('a', 40, hold=6)      # USAR
        g.press('a', 50, hold=6)      # first mon
        for _ in range(ups):
            g.press('up', 8, hold=4)
        g.press('a', 50, hold=6)      # confirm quantity
        texts = []
        last_change = 0
        for k in range(400):
            rows = decode_rows(g, range(12, 18))
            forget = any(('olvidar' in r.lower() or '¿Cuál' in r) for r in rows)
            g.press('a', 16, hold=4)
            g.p.tick(10)
            if crashed(g):
                item['crash'] = 'press %d' % k; item['shot'] = shot(g, 'candy_crash_%d_%d' % (sp, level)); return item
            t = ' / '.join(r[1:-1].strip() for r in decode_rows(g, range(13, 17)) if r[1:-1].strip())
            if t and t not in texts:
                texts.append(t[:70]); last_change = k
            if k - last_change > 60:
                break
            if settled(g) and not any('+' in r for r in decode_rows(g, range(12, 18))) and k > 30 and k - last_change > 25:
                break
        if settled(g):
            item['species_after'] = g.party_species()[0]
            item['level_after'] = g.p.memory[g.a('wPartyMon1Level')]
            item['moves'] = list(g.p.memory[g.a('wPartyMon1Moves'):g.a('wPartyMon1Moves') + 4])
        item['n_texts'] = len(texts); item['last'] = texts[-3:]
        return item
    except Exception as e:
        item['error'] = repr(e)[:150]
        return item
    finally:
        g.close()


for sp in species_list:
    res['mons'].append(one(sp))
print('RESULT ' + json.dumps(res, ensure_ascii=True))
