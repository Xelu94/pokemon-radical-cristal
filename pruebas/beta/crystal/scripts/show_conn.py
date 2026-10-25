import json, sys
tot = nc = 0
for l in open(sys.argv[1], encoding='utf8'):
    r = json.loads(l)
    if r.get('hang') or 'error' in r:
        print('JOB', r['job'], r.get('error', 'HANG')[:200]); continue
    for x in r['results']:
        tot += 1
        if x.get('no_crossing'): nc += 1; print('NOCROSS', x['from'], x['dir'], x['to']); continue
        if x.get('error'): print('ERR', x); continue
        if x['audit'] or x['issues'] or x['missing_from_list']:
            print(x['from'], x['dir'], x['to'], 'audit', x['audit'][:3], 'issues', [i[2][:2] for i in x['issues']][:2], 'missing', x['missing_from_list'])
print('connections', tot, 'nocross', nc)
