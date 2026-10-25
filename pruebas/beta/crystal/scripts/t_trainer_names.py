"""Cross-check the trainer intro line seen in game ('<NAME> <CLASS> quiere luchar.') against the source:
class name from data/trainers/class_names.asm for the `trainer CLASS, ID` line of the object's script.
usage: py -3.12 scripts/t_trainer_names.py logs/npc_g1_h14.jsonl"""
import sys, re, json
from pathlib import Path
ROOT = Path('work/source')
cn = [m for m in re.findall(r'^\s*li "([^"]*)"', (ROOT / 'data/trainers/class_names.asm').read_text(encoding='utf8'), re.M)]
consts = []
for l in (ROOT / 'constants/trainer_constants.asm').read_text(encoding='utf8').splitlines():
    m = re.match(r'\s*trainerclass (\w+)', l)
    if m:
        consts.append(m[1])
print('classes in constants', len(consts), 'names', len(cn))
cname = {c: cn[i - 1] for i, c in enumerate(consts) if i >= 1}
# the names list has an unnamed first entry? align by comparing lengths
mapsrc = {}
for f in (ROOT / 'maps').glob('*.asm'):
    mapsrc[f.stem] = f.read_text(encoding='utf8')
bad = 0; n = 0
for l in open(sys.argv[1], encoding='utf8'):
    r = json.loads(l)
    if 'objects' not in r:
        continue
    src = mapsrc.get(r['map'], '')
    for o in r['objects']:
        if o['type'] != 'OBJECTTYPE_TRAINER':
            continue
        m = re.search(r'^%s:\s*\n\s*trainer (\w+), (\w+)' % re.escape(o['script']), src, re.M)
        if not m:
            continue
        cls = m[1]
        want = cname.get(cls)
        seen = [f for f in o.get('frames', []) if 'quiere' in f]
        if not seen:
            continue
        n += 1
        txt = seen[0]
        want = (want or '').replace('#', 'POKé').replace('POKé MANÍACO', 'POKéMANÍACO')
        if want and want not in txt:
            bad += 1
            print('MISMATCH', r['map'], o['script'], cls, 'expected class name', want, 'saw', txt)
print('checked', n, 'mismatches', bad)
