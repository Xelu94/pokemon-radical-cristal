import json, sys, collections
c = collections.Counter(); bad = []
for l in open(sys.argv[1], encoding='utf8'):
    r = json.loads(l)
    if r.get('hang'): print('HANG', r['job']); continue
    if 'error' in r: print('ERR', r['job'], r['error'][:200]); continue
    for m in r['moves']:
        c[(r['mode'], 'crash' if m.get('crash') else 'err' if m.get('error') else 'ok')] += 1
        if m.get('crash') or m.get('error'):
            print(r['mode'], m['id'], m['name'], m.get('crash'), m.get('error', '')[:100], m.get('shot'))
print(c)
