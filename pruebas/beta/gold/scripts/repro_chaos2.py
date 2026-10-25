"""Same as repro_chaos but with hooks on the rst vectors to catch the first wild jump; prints the caller (stack) and symbol lookups.
usage: repro_chaos2.py worker it seed"""
import json, random, sys, bisect
from lib import *
from read_jsonl import load
w, it, sd = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
rec = [r for r in load('logs/chaos_*.jsonl') if r['worker'] == w and r['it'] == it][0]
spec = rec['spec']
syms = sorted((b * 0x10000 + a, n) for n, (b, a) in ((n, v) for n, v in G.__dict__.get('_x', {}).items())) if False else None
g = G('NEW_BARK_TOWN', 4, 2)
tab = {}
for name, (bank, addr) in g.symbols.items():
    tab.setdefault(bank, []).append((addr, name))
for b in tab: tab[b].sort()
def sym(bank, addr):
    l = tab.get(bank, []); i = bisect.bisect_right([a for a, n in l], addr) - 1
    return '%s+%d' % (l[i][1], addr - l[i][0]) if i >= 0 else hex(addr)
events = []
ring = []
def vec(ctx):
    r = g.p.register_file
    sp = r.SP
    ret = g.p.memory[sp] | g.p.memory[sp + 1] << 8
    if not events:
        st = {n: g.p.memory[g.a(n)] for n in ('wCurEnemyMove','wCurPlayerMove','hBattleTurn','wEnemyMoveStructEffect','wPlayerMoveStructEffect','wBattleMonItem','wEnemyMonItem','wPlayerSubStatus5','wEnemyTurnsTaken','wPlayerTurnsTaken')}
        print('STATE', st)
        sp = r.SP
        words = [g.p.memory[sp + 2 * k] | g.p.memory[sp + 1 + 2 * k] << 8 for k in range(28)]
        out = []
        for wd in words:
            if wd < 0x4000: out.append(sym(0, wd))
            elif wd < 0x8000: out.append('%s|%s|%s' % (hex(wd), sym(0xf, wd), sym(0x20, wd)))
            else: out.append(hex(wd))
        print('STACK', out)
    events.append((ctx, r.PC, hex(ret), hex(g.p.memory[g.a('hROMBank')]), [hex(g.p.memory[sp + 2 + 2 * k] | g.p.memory[sp + 3 + 2 * k] << 8) for k in range(4)]))
def tx(ctx):
    r = g.p.register_file
    ring.append((hex(r.HL), hex(g.p.memory[g.a('hROMBank')]), ctx))
    del ring[:-8]
for nm in ('PrintText', 'PrintTextboxText', 'DoTextUntilTerminator', 'PlaceString', 'PrintLetterDelay'):
    if nm in g.symbols:
        b, a = g.symbols[nm]
        if nm in ('PrintText', 'PrintTextboxText'):
            g.p.hook_register(b, a, lambda c: tx(c), nm)
for v in (0x00, 0x38, 0x100):
    g.p.hook_register(0, v, lambda c: vec(c), v)
strong_party(g, species=spec['species'], level=spec['level'])
mx = spec['maxhp']; hp = max(1, mx * spec['hpfrac'] // 100)
a = g.a('wPartyMon1MaxHP'); g.p.memory[a:a + 2] = [mx >> 8, mx & 255]
a = g.a('wPartyMon1HP'); g.p.memory[a:a + 2] = [hp >> 8, hp & 255]
g.p.memory[g.a('wPartyMon1Moves'):g.a('wPartyMon1Moves') + 4] = spec['moves']
g.p.memory[g.a('wPartyMon1PP'):g.a('wPartyMon1PP') + 4] = [30] * 4
g.p.memory[g.a('wPartyMon1Item')] = spec['item']
g.write('wNewBarkTownSceneID', 1)
g.p.tick(30); g.press('left', 20, hold=16)
rng = random.Random(sd)
injected = False
events.clear()
for i in range(260):
    hist = None
    if rng.random() < 0.3 and injected and battle_menu(g):
        g.press('a', 20, hold=6)
        for _ in range(3): g.press('up', 4, hold=4)
        for _ in range(rng.randint(0, 3)): g.press('down', 4, hold=4)
    g.press('a', 22, hold=6)
    if events:
        print('first vector event at press', i, events[:4]); break
    if not injected and (g.p.memory[0xff70] & 7) == 1 and g.read('wBattleMode') == 2 and g.read('wEnemyMonSpecies') and battle_menu(g):
        g.p.memory[g.a('wEnemyMonMoves'):g.a('wEnemyMonMoves') + 4] = spec['emoves']
        g.p.memory[g.a('wEnemyMonPP'):g.a('wEnemyMonPP') + 4] = [30] * 4
        g.p.memory[g.a('wEnemyMonItem')] = spec['eitem']
        e = spec['emax']; h = min(spec['ehp'], e)
        a = g.a('wEnemyMonMaxHP'); g.p.memory[a:a + 2] = [e >> 8, e & 255]
        a = g.a('wEnemyMonHP'); g.p.memory[a:a + 2] = [h >> 8, h & 255]
        injected = True
print('last text calls', ring)
for ev in events[:3]:
    print(ev, [sym(0, int(x, 16)) for x in ev[4][:1]], sym(0, int(ev[2], 16)))
g.close()
