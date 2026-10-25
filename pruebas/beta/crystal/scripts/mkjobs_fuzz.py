import sys, json
sys.path.insert(0, 'scripts')
from lib import *
SKIP = ('ELEVATOR', 'TRADE_CENTER', 'COLOSSEUM', 'TIME_CAPSULE', 'MOBILE', 'COPYCATS_HOUSE_2F', 'BATTLE_TOWER')
seed = sys.argv[1]; steps = sys.argv[2]; out = sys.argv[3]
cat = [c for c in catalog() if not any(k in c[4] for k in SKIP)]
json.dump([[c[4], seed, steps] for c in cat], open(out, 'w'))
print(len(cat))
