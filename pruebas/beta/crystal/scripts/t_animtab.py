import re
t = open('work/source/data/moves/animations.asm', encoding='utf8').read()
i = t.index('BattleAnimations::') if 'BattleAnimations::' in t else t.index('BattleAnimations:')
tab = re.findall(r'^\s*dw (BattleAnim_\w+)(.*)$', t[i:], re.M)
names = {}
n = -1
for l in open('work/source/constants/move_constants.asm', encoding='utf8'):
    m = re.match(r'\s*const (\w+)', l)
    if m and 'const_def' not in l:
        n += 1; names[n] = m[1]
# the table ends at the first non-dw line group
lines = t[i:].splitlines()
ents = []
for l in lines[1:]:
    m = re.match(r'\s*dw (\w+)\s*(;.*)?$', l)
    if m: ents.append(m[1])
    elif l.strip() and not l.strip().startswith(('table_width', ';', 'assert')): break
print('entries', len(ents))
for k in (0, 1, 2, 175, 176, 177, 178, 179, 180, 181, 250, 251, 252, 253, 254, 255, 256, 257, 258):
    if k < len(ents): print(k, names.get(k), ents[k])
