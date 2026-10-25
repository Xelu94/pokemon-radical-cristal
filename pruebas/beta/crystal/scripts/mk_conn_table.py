import json, sys
def load(fn):
    out = {}
    for l in open(fn, encoding='utf8'):
        r = json.loads(l)
        for x in r.get('results', []):
            out[(x['from'], x['to'])] = x
    return out
g1 = load('logs/conn_g1.jsonl'); g0 = load('logs/conn_g0.jsonl')
rows = []
for k in sorted(set(g1) | set(g0)):
    a = g1.get(k); b = g0.get(k)
    def desc(x):
        if not x or x.get('no_crossing') or x.get('error'): return None
        miss = {}
        for idx, name in x['missing_from_list']:
            miss[name.replace('SPRITE_', '')] = miss.get(name.replace('SPRITE_', ''), 0) + 1
        hw = [i for i in x['audit'] if i[0] == 'HIGHWALK']
        return miss, [h[2].replace('SPRITE_', '') for h in hw], [i for i in x['audit'] if i[0] == 'NOSLOT']
    d1, d0 = desc(a), desc(b)
    if not d1 and not d0: continue
    d = d1 or d0
    if not d[0] and not d[1] and not d[2]: continue
    rows.append((k, d1, d0))
print('| From -> To | NPC sprites missing from the list (drawn with the player graphics) | walker stuck in VRAM bank 0 | note |')
print('|---|---|---|---|')
for k, d1, d0 in rows:
    d = d1 or d0
    miss = ', '.join('%s%s' % (n, (' x%d' % c) if c > 1 else '') for n, c in d[0].items())
    hw = ', '.join(d[1])
    note = ''
    if d1 and d0 and d1[0] != d0[0]: note = 'girl: %s / boy: %s' % (', '.join(d1[0]), ', '.join(d0[0]))
    print('| %s -> %s | %s | %s | %s |' % (k[0], k[1], miss, hw, note))
print(len(rows))
