"""BUG-003 repro: Choice item lock -> choosing another move prints the lock text via StdBattleTextbox from the wrong ROM bank -> reset.
New Bark ambush, Mewtwo holding the item, moves [HARDEN, PSYCHIC]. Turn 1: HARDEN (locks it). Turn 2: select PSYCHIC -> crash.
usage: repro_choice_crash.py [item_hex ...]   (default 2d 32 5a: CHOICE_BAND, SPECS, SCARF; 00 = control without an item)"""
import sys
from lib import *
arm(600)
for it in [int(a, 16) for a in sys.argv[1:]] or [0x2d, 0x32, 0x5a, 0x00]:
    g = G('NEW_BARK_TOWN', 4, 2)
    resets = []
    g.p.hook_register(0, 0x0100, lambda c: resets.append(1), None)
    strong_party(g, moves=(106, 94))
    g.p.memory[g.a('wPartyMon1Item')] = it
    g.write('wNewBarkTownSceneID', 1)
    g.p.tick(30); g.press('left', 20, hold=16)
    for i in range(120):
        if battle_menu(g): break
        g.press('a', 25, hold=6)
    g.press('up', 4, hold=4); g.press('left', 4, hold=4)
    g.press('a', 20, hold=6)                    # LUCHA
    select_move(g, 1)
    g.press('a', 20, hold=6)                    # HARDEN
    for i in range(80):
        if battle_menu(g): break
        g.press('a', 25, hold=6)
    g.press('up', 4, hold=4); g.press('left', 4, hold=4)
    g.press('a', 20, hold=6)                    # LUCHA again
    select_move(g, 2)                           # cursor on PSYCHIC
    g.press('a', 20, hold=6)
    out = 'no crash'
    for i in range(60):
        g.press('a', 25, hold=6)
        t = ' '.join(g.screen_text())
        if 'cartucho' in t or resets: out = 'CRASH (reset) after %d presses' % i; break
        if 'fija' in ' '.join(screen_text2(g)):
            out = 'lock text shown (ok)'; break
    print('item %02x: %s' % (it, out), flush=True)
    shot(g, 'choice_%02x' % it)
    g.close()
