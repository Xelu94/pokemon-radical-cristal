"""Static scan: every string literal of the assembly sources that contains a character with no charmap entry
(such a character is assembled as its raw UTF-8 bytes and shows up as garbage glyphs in game).  -> logs/charscan.txt"""
import re
from pathlib import Path
ROOT = Path('work/source')
cm = set()
for l in (ROOT / 'constants/charmap.asm').read_text(encoding='utf8').splitlines():
    m = re.match(r'\s*charmap "(.+?)",', l)
    if m:
        cm.add(m[1])
toks = sorted(cm, key=len, reverse=True)


def unmapped(s):
    out = []
    i = 0
    while i < len(s):
        for t in toks:
            if s.startswith(t, i):
                i += len(t)
                break
        else:
            out.append(s[i])
            i += 1
    return out


bad = []
for f in list(ROOT.rglob('*.asm')):
    if 'charmap' in f.name or f.parts[-2] in ('macros',):
        continue
    for n, raw in enumerate(f.read_text(encoding='utf8').splitlines(), 1):
        if raw.lstrip().startswith(';'):
            continue
        for m in re.finditer(r'"((?:[^"\\]|\\.)*)"', raw):
            s = m[1]
            if not re.search(r'[^\x00-\x7f]', s):
                continue
            u = [c for c in unmapped(s) if c != ' ']
            if u:
                bad.append((str(f.relative_to(ROOT)), n, ascii(''.join(sorted(set(u)))), ascii(s)))
print('unmapped-char strings:', len(bad))
with open('logs/charscan.txt', 'w', encoding='utf8') as o:
    for b in bad:
        o.write('%s:%d %s | %s\n' % b)
for b in bad[:40]:
    print('%s:%d %s | %s' % b)
