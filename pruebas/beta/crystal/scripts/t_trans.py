"""Walk through every warp (door) of every map: spawn next to it, step through, step back, step through again, and after
each arrival run fullcheck (VRAM of every object's tile vs ROM graphics) + audit (struct tile vs sprite list).
usage: py -3.12 -W ignore scripts/t_trans.py [procs=3] [limit]
Output: logs/trans_g<gender>.txt
"""
import sys, multiprocessing as mp, json
sys.path.insert(0, 'scripts')
from lib import *

SKIP = ('ELEVATOR', 'LINK', 'TRADE', 'COLOSSEUM', 'TIME_CAPSULE', 'MOBILE', 'BATTLE_TOWER', 'PLAYERS_HOUSE_2F', 'COPYCATS_HOUSE_2F')


def warps():
    out = []
    names = re.findall(r'^\s*map (\w+),', (root / 'data/maps/maps.asm').read_text(encoding='utf8'), re.M)
    consts = re.findall(r'^\s*map_const (\w+)', (root / 'constants/map_constants.asm').read_text(encoding='utf8'), re.M)
    table = dict(zip(names, consts))
    for f in sorted((root / 'maps').glob('*.asm')):
        text = f.read_text(encoding='utf8')
        for m in re.finditer(r'^\s*warp_event\s+(\d+),\s*(\d+),\s*(\w+),\s*(\d+)', text, re.M):
            if f.stem in table:
                out.append((table[f.stem], int(m[1]), int(m[2]), m[3]))
    return out


def one(job):
    mapname, x, y, dest = job
    if mapname not in maps or dest not in maps:
        return job, 'skip'
    try:
        g = G(mapname, x, y - 1)
        g.p.tick(60)
        log = []

        def check(label, wait=150):
            g.p.tick(wait)
            fc = fullcheck(g); au = audit(g)
            if fc or au:
                log.append((label, curmap(g), fc, au))

        start = g.mem('wMapGroup', 2)
        g.press('down', 24, hold=16)
        g.p.tick(60)
        after = g.mem('wMapGroup', 2)
        if after == start or after != maps[dest]:
            g.close()
            return job, 'nomove'
        check('out', 90)
        g.press('up', 24, hold=16)
        g.p.tick(60)
        if g.mem('wMapGroup', 2) == maps[dest]:
            g.press('up', 24, hold=16)
        check('in', 90)
        g.press('down', 24, hold=16)
        check('out2', 90)
        g.close()
        return job, log
    except Exception as e:
        return job, 'ERR ' + repr(e)[:80]


if __name__ == '__main__':
    alarm(3400)
    procs = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 9
    jobs, seen = [], set()
    for mapname, x, y, dest in warps():
        key = (mapname, x, y)
        if key in seen or y < 3:
            continue
        seen.add(key)
        jobs.append((mapname, x, y, dest))
    jobs = [j for j in jobs if not any(k in j[0].upper() for k in SKIP)][:limit]
    print('jobs', len(jobs), flush=True)
    stats = {'ok': 0, 'bad': 0, 'nomove': 0, 'skip': 0, 'err': 0}
    gender = os.environ.get('PLAYER_GENDER', '0')
    f = open('logs/trans_g%s.txt' % gender, 'w')
    with mp.Pool(procs) as pool:
        for job, res in pool.imap_unordered(one, jobs, chunksize=4):
            if res == 'nomove': stats['nomove'] += 1
            elif res == 'skip': stats['skip'] += 1
            elif isinstance(res, str): stats['err'] += 1; f.write('ERR %s %s\n' % (job, res)); f.flush()
            elif res: stats['bad'] += 1; f.write('BAD %s %s\n' % (job, res)); f.flush()
            else: stats['ok'] += 1
    f.write(str(stats) + '\n')
    print(stats)
