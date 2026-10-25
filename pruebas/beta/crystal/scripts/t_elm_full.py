"""Elm's duel reward with a FULL party (6) and with the current PC box full: the three shiny starters must go to the PC, no crash.
usage: py -3.12 -W ignore scripts/t_elm_full.py [party6|box_full|both]   (PLAYER_GENDER env)"""
import sys, os
sys.path.insert(0, 'scripts')
from lib import *
alarm(560)
mode = sys.argv[1] if len(sys.argv) > 1 else 'party6'
g = G('NEW_BARK_TOWN', 6, 4)
strong_party(g, level=100)
if mode in ('party6', 'both'):
    g.party([150, 25, 19, 16, 10, 13], level=40)
    strong_party(g, species=150, level=100)
    stride = g.a('wPartyMon2') - g.a('wPartyMon1')
    g.write('wPartyCount', 6)
    for i, sp in enumerate([150, 25, 19, 16, 10, 13]):
        g.p.memory[g.a('wPartySpecies') + i] = sp
        base = g.a('wPartyMon1') + stride * i
        g.p.memory[base] = sp
        g.p.memory[g.a('wPartyMon1Level') + stride * i] = 40 if i else 100
        for stat in ['MaxHP', 'HP', 'Attack', 'Defense', 'Speed', 'SpclAtk', 'SpclDef']:
            g.p.memory[g.a('wPartyMon1' + stat) + stride * i:g.a('wPartyMon1' + stat) + stride * i + 2] = [3, 231] if i == 0 else [0, 90]
        g.p.memory[g.a('wPartyMon1Moves') + stride * i] = 94 if i == 0 else 33
        g.p.memory[g.a('wPartyMon1PP') + stride * i] = 30
    g.p.memory[g.a('wPartySpecies') + 6] = 255
    for i in range(6):
        at = g.a('wPartyMonNicknames') + 11 * i
        g.p.memory[at:at + 11] = [0x8c, 0x84, 0x96, 0x93, 0x96, 0x8e, 0x50, 0, 0, 0, 0]
g.write('wElmsLabSceneID', 2)
g.p.tick(30)
for _ in range(12):
    g.press('up', 8, hold=14)
g.press('right', 20, hold=16)
texts = []
for i in range(900):
    g.press('a', 26, hold=6)
    if crashed(g):
        print('CRASH at', i); break
    rows = decode_rows(g, range(12, 18))
    if len(rows) >= 6 and rows[0].startswith('+'):
        t = ' / '.join(r[1:-1].strip() for r in rows[1:5] if r[1:-1].strip())
        if t and t not in texts:
            texts.append(t)
    if g.read('wBattleMode') == 0 and settled(g) and g.event('EVENT_ELM_DUEL_DONE') and i > 30:
        break
g.p.tick(120)
if settled(g):
    print('party', g.party_species(), 'duel done', g.event('EVENT_ELM_DUEL_DONE'))
print([t for t in texts if 'caja' in t.lower() or 'PC' in t or 'enviado' in t.lower() or 'FERALIGATR' in t][:10])
g.close()
