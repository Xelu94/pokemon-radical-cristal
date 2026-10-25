"""Static check of the overworld sprite table in the ROM: duplicate / blank graphics, size and type sanity.
usage: py -3.12 -W ignore scripts/t_spritehash.py"""
import sys, hashlib
sys.path.insert(0, 'scripts')
from lib import *
g = G('NEW_BARK_TOWN', 4, 2)
seen = {}
for real in range(1, 0x68):
    src, n, typ = sprite_rom(g, real)
    data = bytes(g.rom[src:src + n * 16 * (1 if typ != 1 else 2)])
    h = hashlib.md5(data).hexdigest()[:8]
    blank = not any(data)
    seen.setdefault(h, []).append(sname(real))
    print('%3d %-26s tiles=%2d type=%s md5=%s%s' % (real, sname(real), n, STYPE_NAME.get(typ), h, ' BLANK' if blank else ''))
print('DUPLICATES:', {h: v for h, v in seen.items() if len(v) > 1})
g.close()
