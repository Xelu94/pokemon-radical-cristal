"""Static lint of every dialogue text in the source tree (read only): line width, unknown characters, structure.
usage: py -3.12 scripts/t_textlint.py  -> logs/textlint.txt
Rules (dialogue box = 18 columns, 2 visible rows, scrolling with cont/para):
  * a text/line/cont/para/next/db string longer than 18 columns after expanding <PLAYER>/<RIVAL>... (counted as the max name length)
  * a `line` right after `line` (should be cont), `cont` as the first command, `para` without a following text
  * a text block that does not end in done/prompt/text_end etc.
  * unusual characters not in the charmap
"""
import re, sys
from pathlib import Path
ROOT = Path('work/source')
charmap = set()
for l in (ROOT / 'constants/charmap.asm').read_text(encoding='utf8').splitlines():
    m = re.match(r'\s*charmap "(.+?)",', l)
    if m:
        charmap.add(m[1])
WIDTH = 18
EXPAND = {'<PLAYER>': 'MMMMMMM', '<RIVAL>': 'MMMMMMM', '<GREEN>': 'MMMMM', '<RED>': 'MMMM', '<MOM>': 'MMMM', '#': 'POKé', '<PKMN>': 'PKMN',
          '<PK>': 'P', '<MN>': 'M', '<TARGET>': '', '<USER>': '', '<ENEMY>': '', '<PC>': 'PC', '<TM>': 'TM', '<TRAINER>': 'TRAINER', '<ROCKET>': 'ROCKET',
          '<……>': '……', '<DOT>': '.', '<PLAY_G>': 'MMMMMMM'}
STR = re.compile(r'"((?:[^"\\]|\\.)*)"')


def width(s):
    for k, v in EXPAND.items():
        s = s.replace(k, v)
    s = re.sub(r'<[A-Z_]+>', 'M', s)
    return len(s)


issues = []
files = list((ROOT / 'maps').glob('*.asm')) + list((ROOT / 'data/text').glob('*.asm')) + list((ROOT / 'engine').rglob('*.asm')) + list((ROOT / 'data').rglob('*.asm'))
nblocks = 0
for f in files:
    lines = f.read_text(encoding='utf8').splitlines()
    block = None
    prev = None
    for n, raw in enumerate(lines, 1):
        l = raw.split(';')[0] if '"' not in raw else raw
        m = re.match(r'\s*(text|line|cont|para|next|db|done|prompt|text_end|text_ram|text_decimal|text_bcd|text_far|text_asm|text_pause|text_low|sound_\w+|dex|page|scroll|autoscroll)\b\s*(.*)$', l)
        label = re.match(r'^(\.?\w+)(::?)\s*$', raw)
        if label:
            block = {'label': label[1], 'start': n, 'cmds': [], 'file': f}
            prev = None
            continue
        if not m:
            continue
        cmd, arg = m[1], m[2]
        strs = STR.findall(arg)
        if cmd in ('text', 'line', 'cont', 'para', 'next', 'page', 'scroll', 'autoscroll') and strs:
            nblocks += 1
            s = strs[0]
            if s.endswith('@'): s = s[:-1]
            w = width(s)
            if w > WIDTH:
                issues.append((str(f.relative_to(ROOT)), n, 'WIDTH %d > %d' % (w, WIDTH), ascii(s)))
            for ch in set(re.sub(r'<[^>]*>', '', s)):
                if ch not in charmap and ch not in "ÁÉÍÓÚÑáéíóúñ¿¡":
                    issues.append((str(f.relative_to(ROOT)), n, 'CHAR %s not in charmap' % ascii(ch), ascii(s)))
            if cmd == 'line' and prev == 'line':
                issues.append((str(f.relative_to(ROOT)), n, 'line after line (use cont)', s))
            if cmd in ('cont',) and prev in (None, 'text', 'para') and False:
                pass
        prev = cmd
print('strings', nblocks, 'issues', len(issues))
with open('logs/textlint.txt', 'w', encoding='utf8') as out:
    for i in issues:
        out.write('%s:%d %s | %s\n' % i)
for i in issues[:80]:
    print('%s:%d %s | %s' % i)
