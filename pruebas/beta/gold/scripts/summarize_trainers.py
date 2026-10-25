import sys; sys.path.insert(0,'scripts')
from read_jsonl import load
import collections
recs=load(sys.argv[1] if len(sys.argv)>1 else 'logs/trainer_*.jsonl')
print(len(recs), collections.Counter((r.get('fight'), r.get('post')) for r in recs))
for r in recs:
    if r.get('error') or r.get('fight')!='end' or r.get('post')!='done' or r.get('sprite_problems') or (r.get('oam_bad') or 0)>0:
        print(r['map'], r['x'], r['y'], r.get('script'), r.get('fight'), r.get('post'), r.get('error'), r.get('sprite_problems'), r.get('oam_bad'), (r.get('post_pages') or [])[-2:])
print('no money', [(r['map'],r['script']) for r in recs if r.get('fight')=='end' and r.get('money_delta',0)==0][:40])
