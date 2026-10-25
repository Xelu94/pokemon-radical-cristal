from lib import *
table = stem_to_const()
tot_o = tot_b = 0; miss = []
import re
for stem in sorted(table):
    objs, bgs, warps = parse_map(stem)
    text = (SRC / 'maps' / (stem + '.asm')).read_text(encoding='utf8')
    n_o = len(re.findall(r'^\s*object_event', text, re.M)); n_b = len(re.findall(r'^\s*bg_event', text, re.M))
    tot_o += len(objs); tot_b += len(bgs)
    if len(objs) != n_o or len(bgs) != n_b: miss.append((stem, len(objs), n_o, len(bgs), n_b))
print(tot_o, tot_b, miss[:10], len(miss))
print(len([s for s in table if table[s] in maps]), len(table))
