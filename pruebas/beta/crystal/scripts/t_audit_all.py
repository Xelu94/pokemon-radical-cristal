"""Audit sprite slots of every map object of every map (394 maps) at its sandbox spawn point.
usage: py -3.12 -W ignore scripts/t_audit_all.py [procs=3]      (PLAYER_GENDER env respected)
Reports per map object (from wMap1Object.., not only the ones that have an object struct):
  NOSLOT   sprite id missing from wUsedSprites (object will be drawn with the player's tile)
  HIGHWALK WALKING_SPRITE graphic in the bank-0 second table (tile>=0x80): standing frames only
Output: logs/audit_all_<gender>.txt
"""
import sys, multiprocessing as mp, json
sys.path.insert(0, 'scripts')
from lib import *

SKIP = ('ELEVATOR', 'TRADE_CENTER', 'COLOSSEUM', 'TIME_CAPSULE', 'MOBILE', 'COPYCATS_HOUSE_2F')


def one(entry):
    gi, num, x, y, name = entry
    maps[name] = [gi, num]
    try:
        g = G(name, x, y)
        g.p.tick(120)
        res = {'map': name, 'ok': curmap(g) == name, 'n': len(used_sprites(g))}
        slot = {}
        for sid, t in used_sprites(g):
            slot.setdefault(sid, t)
        tiles = sum({1: 12, 2: 12, 3: 4}.get(STYPE.get(realsprite(g, s), 1), 12) for s, _ in used_sprites(g))
        res['tiles'] = tiles
        probs = []
        for k, mo in enumerate(mapobjs(g), 1):
            sprite = mo[1]
            if not sprite:
                continue
            real = realsprite(g, sprite)
            if sprite not in slot:
                probs.append(('NOSLOT', k, sname(sprite), mo[4]))
                continue
            t = slot[sprite]
            if t >= 0x80 and real and real < 0x80 and STYPE.get(real) == 1:
                probs.append(('HIGHWALK', k, sname(sprite), 'mv=%d tile=%d' % (mo[4], t)))
        res['probs'] = probs
        res['list'] = listing(g)
        g.close()
        return res
    except Exception as e:
        return {'map': name, 'error': repr(e)}


if __name__ == '__main__':
    alarm(3000)
    procs = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    cat = [c for c in catalog() if not any(k in c[4] for k in SKIP)]
    out = []
    with mp.Pool(procs) as pool:
        for r in pool.imap_unordered(one, cat, chunksize=4):
            out.append(r)
    out.sort(key=lambda r: r['map'])
    gender = os.environ.get('PLAYER_GENDER', '0')
    Path('logs').mkdir(exist_ok=True)
    json.dump(out, open('logs/audit_all_g%s.json' % gender, 'w'), indent=1)
    with open('logs/audit_all_g%s.txt' % gender, 'w') as f:
        for r in out:
            if 'error' in r:
                f.write('%s ERROR %s\n' % (r['map'], r['error'])); continue
            if r['probs'] or not r['ok']:
                f.write('%s ok=%s list=%d tiles=%d %s\n' % (r['map'], r['ok'], r['n'], r['tiles'], r['probs']))
    bad = [r for r in out if r.get('probs') or 'error' in r or not r.get('ok')]
    print('maps', len(out), 'with problems', len(bad))
    for r in bad[:80]:
        print(r['map'], r.get('probs') or r.get('error') or 'not loaded')
