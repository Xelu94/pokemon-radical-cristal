from lib import *
g = G('NEW_BARK_TOWN', 4, 2, init=False)
for i in range(1, 0x68):
    off, n, typ = rom_sprite(g, i)
    print('%02x %-28s %-8s tiles=%d' % (i, sprite_name(i), TYPES.get(typ), n))
g.close()
