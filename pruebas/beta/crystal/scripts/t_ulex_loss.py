"""Ulex encounter with a weak party (loss): prints every dialogue page, final map, party and the Nuzlocke state.
usage: py -3.12 -W ignore scripts/t_ulex_loss.py <MapStem> <objidx> [badges=0|255] [party=weak|one]"""
import sys, os
sys.path.insert(0, 'scripts')
from lib import *
import objs
alarm(500)
stem, idx = sys.argv[1], int(sys.argv[2])
badges = int(sys.argv[3]) if len(sys.argv) > 3 else 255
const = objs.const_of(stem)
o = [x for x in objs.parse_map(stem)['objects'] if x['idx'] == idx][0]
OVERRIDES['clear'] = [o['flag']]
g = G(const, o['x'], o['y'] + 1)
g.party([19, 16, 10] if (len(sys.argv) < 5 or sys.argv[4] == 'weak') else [19], level=5)
for i_ in range(3):
    at_ = g.a('wPartyMonNicknames') + 11 * i_
    g.p.memory[at_:at_ + 11] = [0x8c, 0x84, 0x96, 0x93, 0x96, 0x8e, 0x50, 0, 0, 0, 0]
g.p.memory[g.a('wPlayerName'):g.a('wPlayerName') + 5] = [0x93, 0x88, 0x93, 0x8e, 0x50]
g.write('wJohtoBadges', badges)
g.p.tick(40)
print('party before', g.party_species(), 'map', curmap(g))
g.press('up', 12, hold=6)
seen = []
for i in range(1600):
    if any('¿Qu' in r_ for r_ in decode_rows(g, range(13, 18))):
        g.press('down', 14, hold=5); g.press('down', 14, hold=5)
    g.press('a', 24, hold=5)
    if crashed(g):
        print('CRASH at', i); break
    rows = decode_rows(g, range(12, 18))
    if len(rows) >= 6 and rows[0].startswith('+'):
        t = ' / '.join(r[1:-1].strip() for r in rows[1:5] if r[1:-1].strip())
        if t and t not in seen:
            seen.append(t)
    if i > 40 and g.read('wBattleMode') == 0 and settled(g) and i % 20 == 0:
        pass
g.p.tick(120)
print('map after', curmap(g), 'pos', g.pos())
if settled(g):
    print('party after', g.party_species(), 'dead flags/ended', g.read('wNuzlockeRunEnded') if 'wNuzlockeRunEnded' in g.symbols else '?')
for t in seen:
    print('  |', t)
shot(g, 'ulex_loss_%s' % stem)
g.close()
