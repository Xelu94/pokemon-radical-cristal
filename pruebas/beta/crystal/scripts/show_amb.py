import json, sys, subprocess
for s in sys.argv[2:]:
    out = subprocess.run(['py','-3.12','-W','ignore','scripts/w_ambush.py',s], capture_output=True, text=True, encoding='utf8', errors='replace').stdout
    line = [l for l in out.splitlines() if l.startswith('RESULT ')]
    if not line: print(s, 'NO RESULT', out[-300:]); continue
    r = json.loads(line[0][7:])
    print('===', s, 'gender', r['gender'], 'map', r.get('map'), 'err', r.get('error','')[:200])
    print('  flags', r.get('flags'), 'bag', r.get('bag'), 'party', r.get('party'))
    print('  issues', r['issues'][:4])
    for t in r['texts'][:40]: print('   |', t)
