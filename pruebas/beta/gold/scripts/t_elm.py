"""Elm duel in the INITIALISED state (lib.G), as in work/test-v45-story.py, with progress logging."""
import sys
from lib import *
arm(900)
init = (sys.argv[1] if len(sys.argv) > 1 else '1') == '1'
g = G('NEW_BARK_TOWN', 6, 4, init=init)
if len(sys.argv) > 2 and sys.argv[2] == 'lead':
    g.party([150], level=100)
    for stat in ['MaxHP', 'HP', 'Attack', 'Defense', 'Speed', 'SpclAtk', 'SpclDef']:
        g.p.memory[g.a('wPartyMon1' + stat):g.a('wPartyMon1' + stat) + 2] = [3, 231]
    g.p.memory[g.a('wPartyMon1Moves')] = 94; g.p.memory[g.a('wPartyMon1PP')] = 30
    g.write('wJohtoBadges', 0xff); g.write('wKantoBadges', 0xff)
    at = g.a('wPartyMonNicknames'); g.p.memory[at:at + 11] = [0x8c, 0x84, 0x96, 0x93, 0x96, 0x8e, 0x50, 0, 0, 0, 0]
else:
    strong_party(g)
g.write('wElmsLabSceneID', 2)
for _ in range(12): g.press('up', 8, hold=14)
g.press('right', 20, hold=16)
last = None
for i in range(1500):
    g.press('a', 30, hold=6)
    if i % 50 == 0 and g.read('wBattleMode') == 0 and (g.p.memory[0xff70] & 7) in (0, 1):
        st = (where(g), g.read('wPartyCount'), tuple(g.party_species()) if g.read('wPartyCount') < 7 else None, g.event('EVENT_ELM_DUEL_DONE'), g.event('EVENT_GOT_MASTER_BALL_FROM_ELM') if 'EVENT_GOT_MASTER_BALL_FROM_ELM' in EVENTS else None)
        if st != last: print(i, st, [t for t in screen_text2(g, range(12, 18)) if t.strip('│┌└┐┘─ ')][:2], flush=True); last = st
    if g.event('EVENT_ELM_DUEL_DONE') and i > 100 and g.read('wBattleMode') == 0:
        break
for i in range(500):
    g.press('a', 30, hold=6)
g.p.tick(120)
print('after extra mash: party', g.party_species(), [g.is_shiny(i) for i in range(len(g.party_species()))], 'exhibition', g.event('EVENT_EXHIBITION_BATTLE'), 'forceshiny', g.event('EVENT_FORCE_SHINY_GIFT'), 'hp1', g.mem('wPartyMon1HP', 2))
print('done', g.event('EVENT_ELM_DUEL_DONE'), 'crashed', crashed(g), where(g) if safe(g) else 'unsafe')
print(chr(10).join(screen_text2(g)))
g.close()
