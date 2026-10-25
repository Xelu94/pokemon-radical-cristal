"""REPRO detail: OAM tiles used by the dude while walking, with the VRAM contents compared against the ROM frames of his sprite.
usage: py -3.12 -W ignore scripts/t_repro_dude2.py newbark|warp"""
import sys; sys.path.insert(0, 'scripts')
from lib import *
alarm(300)
frm = sys.argv[1]
g = G('NEW_BARK_TOWN', 0, 8) if frm == 'newbark' else G('ROUTE_29', 59, 8)
g.write('wRoute29SceneID', 1); g.party([152], level=6); g.p.tick(60)
src, n, typ = sprite_rom(g, 0x23)
rom = g.rom
romtiles = [bytes(rom[src + k * 16:src + k * 16 + 16]) for k in range(n * 2)]   # 12 standing + 12 walking
g.p.button_press('left')
shots = []
rec = []
for i in range(520):
    g.p.tick(1)
    if g.pos()[0] <= 52 and curmap(g) == 'ROUTE_29':
        g.p.button_release('left')
    if curmap(g) != 'ROUTE_29' or not settled(g):
        continue
    s = structs(g)[1]
    if s[0] != 0x23:
        continue
    oam = oam_list(g)
    # entries drawing the dude = those whose tile data equals one of his ROM tiles OR sit in his slot range
    base = s[2]
    lo = base & 0x7f if base >= 0x80 else base
    mine = []
    for (idx, y, x, t, a) in oam:
        bank = (a >> 3) & 1
        data = bytes(g.p.memory[bank, 0x8000 + t * 16:0x8000 + t * 16 + 16])
        which = [k for k, d in enumerate(romtiles) if d == data]
        inrange = (bank == (1 if base < 0x80 else 0)) and (lo <= t < lo + 12 or (base < 0x80 and lo + 0x80 <= t < lo + 0x80 + 12))
        if inrange or which:
            mine.append((t, bank, which[:2], inrange))
    if mine:
        rec.append((i, g.pos(), s[8], s[9], mine))
# print only the frames where an OAM entry in dude's slot has non-matching data
bad = [r for r in rec if any(m[3] and not m[2] for m in r[4])]
print('frames with dude OAM', len(rec), 'with MISMATCH (tile in his slot but data is not his graphics)', len(bad))
for r in bad[:6]:
    print(r)
import collections
c = collections.Counter()
for r in rec:
    for m in r[4]:
        c[(m[0], m[1], tuple(m[2]))] += 1
print('distinct (oamtile, bank, romtile#) seen:', sorted(c.items())[:40])
print('sample ok frame', rec[len(rec)//2] if rec else None)
g.close()
