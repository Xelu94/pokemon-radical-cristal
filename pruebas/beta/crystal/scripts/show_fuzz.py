import json, sys, collections
fn = sys.argv[1]
n = 0
for l in open(fn, encoding='utf8'):
    r = json.loads(l)
    n += 1
    if r.get('hang') or r.get('error') or r.get('issues') or r.get('crash'):
        print(r.get('map') or r['job'], 'HANG' if r.get('hang') else '', r.get('error', '')[:200], 'CRASH' if r.get('crash') else '')
        for i in r.get('issues', [])[:5]:
            print('    ', i[0], i[1], i[2][:3], i[3])
print('total', n)
