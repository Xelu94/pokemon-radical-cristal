import re
t=open('work/source/data/maps/outdoor_sprites.asm',encoding='utf8').read()
blocks=re.split(r'\n(?=\w+GroupSprites:)',t)
for b in blocks:
    m=re.match(r'(\w+GroupSprites):',b)
    if not m: continue
    sp=re.findall(r'^\s*db (SPRITE_\w+)',b,re.M)
    print(m[1],len(sp),'dups' if len(set(sp))!=len(sp) else '')
