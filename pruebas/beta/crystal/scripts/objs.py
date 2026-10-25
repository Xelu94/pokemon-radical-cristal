"""Parse object_event / bg_event / warp_event / coord_event lines of the map sources."""
import re
from pathlib import Path

ROOT = Path('work/source')


def stem_of(const):
    names = re.findall(r'^\s*map (\w+),', (ROOT / 'data/maps/maps.asm').read_text(encoding='utf8'), re.M)
    consts = re.findall(r'^\s*map_const (\w+)', (ROOT / 'constants/map_constants.asm').read_text(encoding='utf8'), re.M)
    return dict(zip(consts, names))[const]


def const_of(stem):
    names = re.findall(r'^\s*map (\w+),', (ROOT / 'data/maps/maps.asm').read_text(encoding='utf8'), re.M)
    consts = re.findall(r'^\s*map_const (\w+)', (ROOT / 'constants/map_constants.asm').read_text(encoding='utf8'), re.M)
    return dict(zip(names, consts))[stem]


def parse_map(stem):
    text = (ROOT / 'maps' / (stem + '.asm')).read_text(encoding='utf8')
    out = {'objects': [], 'bgs': [], 'warps': [], 'coords': []}
    for m in re.finditer(r'^\s*object_event\s+(.*)$', text, re.M):
        f = [x.strip() for x in m[1].split(';')[0].split(',')]
        if len(f) < 13:
            continue
        out['objects'].append(dict(x=int(f[0]), y=int(f[1]), sprite=f[2], move=f[3], r1=f[4], r2=f[5], h1=f[6], h2=f[7],
                                   pal=f[8], type=f[9], sight=f[10], script=f[11], flag=f[12], idx=len(out['objects']) + 1))
    for m in re.finditer(r'^\s*bg_event\s+(\d+),\s*(\d+),\s*(\w+),\s*(\w+)', text, re.M):
        out['bgs'].append(dict(x=int(m[1]), y=int(m[2]), type=m[3], script=m[4]))
    for m in re.finditer(r'^\s*warp_event\s+(\d+),\s*(\d+),\s*(\w+),\s*(-?\d+)', text, re.M):
        out['warps'].append(dict(x=int(m[1]), y=int(m[2]), dest=m[3], n=int(m[4])))
    for m in re.finditer(r'^\s*coord_event\s+(\d+),\s*(\d+),\s*([\w\-]+),\s*(\w+)', text, re.M):
        out['coords'].append(dict(x=int(m[1]), y=int(m[2]), scene=m[3], script=m[4]))
    return out


def all_maps():
    names = re.findall(r'^\s*map (\w+),', (ROOT / 'data/maps/maps.asm').read_text(encoding='utf8'), re.M)
    return names


if __name__ == '__main__':
    import sys
    n = 0
    for s in all_maps():
        p = parse_map(s)
        n += len(p['objects'])
    print('maps', len(all_maps()), 'objects', n)
