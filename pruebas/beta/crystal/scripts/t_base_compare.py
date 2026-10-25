"""Does the Spanish base ROM (build/base0) show the same connection problem?  usage: py -3.12 -W ignore scripts/t_base_compare.py"""
import sys
sys.path.insert(0, 'scripts')
import lib
from pathlib import Path
from lib import *
for label, rootdir in (('base0 (before the hack)', 'C:/Users/xelu3/build/base0'), ('this ROM', 'work/source')):
    lib.root = Path(rootdir)
    globals()['root'] = Path(rootdir)
    for (a, x, y, key, steps) in (('ROUTE_38', 39, 8, 'right', 5), ('NEW_BARK_TOWN', 0, 8, 'left', 4), ('ROUTE_35', 4, 35, 'down', 4)):
        g = lib.G(a, x, y); g.p.tick(60)
        for _ in range(steps):
            g.press(key, 16, hold=18)
        g.p.tick(60)
        slot = {s for s, t in used_sprites(g)}
        miss = [sname(mo[1]) for mo in mapobjs(g) if mo[1] and mo[1] not in slot]
        print(label, a, '->', curmap(g), 'objects missing from list:', miss, 'audit', audit(g)[:2])
        g.close()
