"""Builds gfx/pokemon/dark_lugia/back.png (48x48, the four Dark Lugia colours) from the back view supplied by the
project author: a 60x60 pixel-art sprite enlarged to 1024x1024.

The 60x60 art is sampled at the centre of each enlarged pixel, reduced to the four palette colours, and then shrunk
to 48x48 by coverage: a target pixel is black when at least 35 % of it is black (so outlines survive), white when at
least 55 % of it is white, and otherwise the more covered of the two purples.
Usage: build_dark_lugia_back.py <image>"""
import sys
from pathlib import Path
from PIL import Image

PAL = [(255, 255, 255), (99, 82, 140), (66, 41, 90), (0, 0, 0)]
REF = [(255, 255, 255), (100, 79, 136), (62, 44, 90), (0, 0, 0)]
SOURCE, TARGET = 60, 48


def nearest(c):
    return min(range(4), key=lambda i: sum((c[k] - REF[i][k]) ** 2 for k in range(3)))


def main():
    src = Image.open(sys.argv[1]).convert('RGB')
    step = src.size[0] / SOURCE
    idx = [[nearest(src.getpixel((int((x + 0.5) * step), int((y + 0.5) * step)))) for x in range(SOURCE)] for y in range(SOURCE)]
    scale = SOURCE / TARGET
    out = Image.new('RGB', (TARGET, TARGET))
    for ty in range(TARGET):
        for tx in range(TARGET):
            x0, x1, y0, y1 = tx * scale, (tx + 1) * scale, ty * scale, (ty + 1) * scale
            cover = [0.0] * 4
            for sy in range(int(y0), min(SOURCE, int(y1) + 1)):
                for sx in range(int(x0), min(SOURCE, int(x1) + 1)):
                    w = (min(x1, sx + 1) - max(x0, sx)) * (min(y1, sy + 1) - max(y0, sy))
                    if w > 0:
                        cover[idx[sy][sx]] += w
            total = sum(cover)
            cover = [c / total for c in cover]
            if cover[3] >= 0.35:
                k = 3
            elif cover[0] >= 0.55:
                k = 0
            else:
                k = max((1, 2), key=lambda i: cover[i]) if max(cover[1], cover[2]) > 0 else 0
            out.putpixel((tx, ty), PAL[k])
    out.save(Path('gfx/pokemon/dark_lugia') / 'back.png')


if __name__ == '__main__':
    main()
