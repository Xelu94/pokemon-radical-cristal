"""Static sprite scan of every map of the sandbox catalog on the normal ROM, as a real new game (events initialised),
at several times of day.  Usage: scan_maps.py <worker> <nworkers> [hours,comma] > logs/scan_<worker>.jsonl
Per map reports: NOT_IN_LIST / STALE_TILE / MAPOBJ_DIFF / VRAM_BAD (check_objects) and table-2 walkers (WALKING sprite
in the second VRAM table = no walking frames) with the object's movement type."""
import json, sys, time
sys.path.insert(0, 'C:/Users/xelu3/build')
from lib import *
from smoke_maps import catalog

worker, nworkers = int(sys.argv[1]), int(sys.argv[2])
hours = [int(h) for h in (sys.argv[3] if len(sys.argv) > 3 else '20,12,6').split(',')]
cat = [c for c in catalog() if not any(k in c[4] for k in ('ELEVATOR', 'POKECENTER_2F', 'TRADE_CENTER', 'COLOSSEUM', 'TIME_CAPSULE', 'MOBILE', 'COPYCATS_HOUSE_2F'))]
cat = cat[worker::nworkers]
arm(3000)
MOVE_WALKS = {2, 4, 5, 0xb, 0xc, 0xd, 0x13, 0x14}
for gi, num, x, y, name in cat:
    maps[name] = [gi, num]
    for hour in hours:
        rec = dict(map=name, hour=hour)
        try:
            g = G(name, x, y, hour=hour)
            g.p.tick(120)
            rec['ok'] = g.mem('wMapGroup', 2) == [gi, num]
            rec['n_used'] = len(used(g))
            rec['problems'] = check_objects(g)
            mo = mapobj_slots(g)
            rec['mapobjs'] = mo
            rec['missing'] = [o for o in mo if o['slot'] is None and o['type'] is not None]
            rec['t2walk'] = [o for o in mo if o['slot'] is not None and o['slot'] >= 0x80 and o['type'] == 'WALKING' and o['move'] in MOVE_WALKS]
            rec['t2any'] = [o for o in mo if o['slot'] is not None and o['slot'] >= 0x80 and o['type'] == 'WALKING']
            # force a RefreshSprites (start menu open/close) and re-check
            g.reload_map()
            g.p.tick(60)
            rec['problems_after_menu'] = check_objects(g)
            rec['mapobjs_after_menu'] = mapobj_slots(g) if rec['mapobjs'] != mapobj_slots(g) else 'same'
            g.close()
        except Exception as e:
            rec['error'] = repr(e)[:200]
        print(json.dumps(rec), flush=True)
