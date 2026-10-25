"""Egg hatching: an egg with hatch counter 1 should hatch after ~10 steps into a random shiny first-stage non-legendary Pokemon.
argv: trials   -> prints species/shiny/steps for every trial (fresh game each time, different RNG by waiting a few frames)"""
import sys, json
sys.path.insert(0, 'scripts')
from lib import *
alarm(580)
trials = int(sys.argv[1]) if len(sys.argv) > 1 else 6
out = []
for t in range(trials):
    g = G('GOLDENROD_CITY', 24, 8)
    try:
        strong_party(g, level=30)
        # add an egg as party member 2: species list [150, EGG]
        stride = g.a('wPartyMon2') - g.a('wPartyMon1')
        g.write('wPartyCount', 2)
        g.p.memory[g.a('wPartySpecies') + 1] = 253
        g.p.memory[g.a('wPartySpecies') + 2] = 255
        base = g.a('wPartyMon2')
        g.p.memory[base:base + stride] = [0] * stride
        g.p.memory[base] = 19                       # internal species (Rattata) of the egg
        g.p.memory[g.a('wPartyMon1Level') + stride] = 1
        g.p.memory[g.a('wPartyMon1Moves') + stride] = 33
        g.p.memory[g.a('wPartyMon1Happiness') + stride] = 1      # hatch counter
        for stat in ['HP', 'MaxHP', 'Attack', 'Defense', 'Speed', 'SpclAtk', 'SpclDef']:
            g.p.memory[g.a('wPartyMon1' + stat) + stride:g.a('wPartyMon1' + stat) + stride + 2] = [0, 10]
        at = g.a('wPartyMonNicknames') + 11
        g.p.memory[at:at + 11] = [0x84, 0x86, 0x86, 0x50, 0, 0, 0, 0, 0, 0, 0]
        g.p.tick(60 + t * 37)
        steps = 0
        hatched = None
        for i in range(40):
            g.press(['left', 'right'][i % 2], 4, hold=16)
            steps += 1
            if g.read('wBattleMode') != 0:
                continue
            for _ in range(2):
                g.p.tick(10)
            t_ = ' '.join(r for r in decode_rows(g, range(12, 18)) if r)
            if 'eclos' in t_.lower() or 'Oh' in t_ or 'EGG' in t_ or 'Huevo' in t_.upper():
                hatched = steps
                break
        for _ in range(60):
            g.press('a', 20, hold=4)
        g.p.tick(60)
        if settled(g):
            sp = g.party_species()
            out.append({'trial': t, 'hatch_step': hatched, 'party': sp, 'shiny': [g.is_shiny(i) for i in range(len(sp))]})
        else:
            out.append({'trial': t, 'unsettled': True})
    finally:
        g.close()
print('RESULT ' + json.dumps(out))
