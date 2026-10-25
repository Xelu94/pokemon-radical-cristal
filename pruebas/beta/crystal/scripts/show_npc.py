import json, sys
fn = sys.argv[1]; out = sys.argv[2]
rows = [json.loads(l) for l in open(fn, encoding='utf8')]
rows.sort(key=lambda r: r.get('map', str(r.get('job'))))
f = open(out, 'w', encoding='utf8')
bad = {'hang': [], 'error': [], 'crash': [], 'garbage': [], 'noresp': [], 'hangtext': [], 'battle': []}
nobj = 0
for r in rows:
    if r.get('hang'): bad['hang'].append(r['job']); continue
    if 'error' in r: bad['error'].append((r['job'], r['error'][:300])); continue
    f.write('=== %s (%s)\n' % (r['map'], r['const']))
    for o in r['objects']:
        nobj += 1
        tag = ''
        if o.get('crash') or 'CRASH' in o.get('flags', []) or 'CRASH_IN_BATTLE' in o.get('flags', []): bad['crash'].append((r['map'], o['idx'], o['script'])); tag += ' CRASH'
        if 'GARBAGE' in o.get('flags', []): bad['garbage'].append((r['map'], o['idx'], o['script'])); tag += ' GARBAGE'
        if 'HANG_TEXT' in o.get('flags', []): bad['hangtext'].append((r['map'], o['idx'], o['script'])); tag += ' HANGTEXT'
        if (o.get('no_response') and not o.get('frames') and not o.get('battle')): bad['noresp'].append((r['map'], o['idx'], o['script'], o['sprite'], o['flag'])); tag += ' NORESP'
        if o.get('battle'): bad['battle'].append((r['map'], o['idx'], o['script'])); tag += ' BATTLE'
        if o.get('error'): bad['error'].append((r['map'], o['idx'], o['error'][:200]))
        f.write('  #%d %s %s %s @%s,%s flag=%s%s\n' % (o['idx'], o['sprite'], o['script'], o['type'].replace('OBJECTTYPE_',''), o['x'], o['y'], o['flag'], tag))
        for fr in o.get('frames', []):
            f.write('      | %s\n' % fr)
print('maps', len(rows), 'objects', nobj)
for k, v in bad.items():
    print(k, len(v))
    if k not in ('noresp', 'battle'):
        for x in v[:40]: print('   ', x)
json.dump(bad, open(out + '.bad.json', 'w'), indent=1)
