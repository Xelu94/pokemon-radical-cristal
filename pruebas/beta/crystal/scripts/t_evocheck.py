import re
t = open('work/source/data/pokemon/evos_attacks.asm', encoding='utf8').read()
blocks = re.split(r'\n(?=\w+EvosAttacks:)', t)
evo = {}
for b in blocks:
    m = re.match(r'(\w+)EvosAttacks:', b)
    if not m: continue
    es = re.findall(r'^\s*db (EVOLVE_\w+), ([^,\n]+)(?:, ([^,\n;]+))?(?:, ([^,\n;]+))?', b, re.M)
    evo[m[1]] = es
for sp in ['Kadabra','Machoke','Graveler','Haunter','Poliwhirl','Slowpoke','Onix','Seadra','Scyther','Porygon','Golbat','Chansey','Pichu','Cleffa','Igglybuff','Togepi','Eevee']:
    print(sp, evo.get(sp))
# all non-level evolution kinds
import collections
c = collections.Counter(e[0] for v in evo.values() for e in v)
print(c)
