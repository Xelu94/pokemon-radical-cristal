"""Contact sheets of all trainer battle intro screens (shots/tr/*.png) captioned with the trainer class constant of the object's script.
usage: py -3.12 scripts/mk_trainer_sheets.py -> shots/trainers_page<N>.png"""
import re, json
from pathlib import Path
from PIL import Image, ImageDraw
ROOT = Path('work/source')
src = {f.stem: f.read_text(encoding='utf8') for f in (ROOT / 'maps').glob('*.asm')}
import sys
sys.path.insert(0, 'scripts')
import objs
items = []
for f in sorted(Path('shots/tr').glob('*.png')):
    stem, idx = f.stem.rsplit('_', 1)
    pm = objs.parse_map(stem)
    o = [x for x in pm['objects'] if x['idx'] == int(idx)][0]
    m = re.search(r'^%s:\s*\n\s*trainer (\w+), (\w+)' % re.escape(o['script']), src[stem], re.M)
    cls = m[1] if m else o['script'][:14]
    items.append((cls, f))
items.sort(key=lambda x: x[0])
W, H = 80, 72
cols, rows = 10, 7
per = cols * rows
for p in range(0, len(items), per):
    page = Image.new('RGB', (cols * W, rows * (H + 10)), (255, 255, 255))
    d = ImageDraw.Draw(page)
    for k, (cls, f) in enumerate(items[p:p + per]):
        im = Image.open(f).resize((W, H), Image.LANCZOS)
        x, y = (k % cols) * W, (k // cols) * (H + 10)
        page.paste(im, (x, y))
        d.text((x + 1, y + H), cls[:13], fill=(200, 0, 0))
    page.save('shots/trainers_page%d.png' % (p // per + 1))
print(len(items), 'trainers,', (len(items) + per - 1) // per, 'pages')
