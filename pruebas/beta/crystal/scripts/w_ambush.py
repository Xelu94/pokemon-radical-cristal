"""Worker: play one of the other-protagonist scenes with the current PLAYER_GENDER and record text, battle intro screens, sprite checks.
argv: scene  (newbark | sprout | dragon | indigo | home)
Writes shots/amb_<scene>_g<gender>_*.png and prints RESULT json (texts, flags, bag, party, issues)."""
import sys, json, traceback
sys.path.insert(0, 'scripts')
from lib import *
alarm(560)
scene = sys.argv[1]
gender = os.environ.get('PLAYER_GENDER', '0')
res = {'scene': scene, 'gender': gender, 'texts': [], 'issues': [], 'battle_shots': []}
if scene == 'dragon':
    OVERRIDES['set'] = ['EVENT_BEAT_RIVAL_IN_MT_MOON']
    OVERRIDES['clear'] = ['EVENT_RIVAL_DRAGONS_DEN']
    os.environ['HOUR'] = '12'; os.environ['DAYNUM'] = '2'
setups = {
    'newbark': ('NEW_BARK_TOWN', 4, 2, 'left'),
    'sprout': ('SPROUT_TOWER_3F', 11, 10, 'up'),
    'dragon': ('DRAGONS_DEN_B1F', 20, 26, 'up'),
    'indigo': ('INDIGO_PLATEAU_POKECENTER_1F', 5, 13, 'up'),
    'home': ('PLAYERS_NEIGHBORS_HOUSE', 3, 7, 'up'),
}
const, x, y, key = setups[scene]
try:
    g = G(const, x, y)
    strong_party(g, level=100 if scene in ('indigo',) else 60)
    if scene == 'home':
        g.set_event('EVENT_OTHER_FINAL_DONE')
    g.p.tick(40)
    w = Watch(g, 'amb_%s_g%s' % (scene, gender))
    if scene == 'dragon':
        # talk to the rival (wanders around (20,23)): walk up to him
        pass
    g.p.button_press(key); g.p.tick(18); g.p.button_release(key)
    seen = set(); last_batt = False; bshots = 0
    for i in range(1100):
        g.press('a', 26, hold=6)
        w.check('a')
        if crashed(g):
            res['issues'].append('CRASH'); break
        rows = decode_rows(g, range(12, 18))
        if len(rows) >= 6 and rows[0].startswith('+'):
            t = ' / '.join(r[1:-1].strip() for r in rows[1:5] if r[1:-1].strip())
            if t and t not in seen:
                seen.add(t); res['texts'].append(t)
        inb = g.read('wBattleMode') != 0
        if inb and bshots < 6 and i % 3 == 0:
            res['battle_shots'].append(shot(g, 'amb_%s_g%s_battle%d' % (scene, gender, bshots))); bshots += 1
        if scene == 'newbark' and g.event('EVENT_OTHER_AMBUSH_NEW_BARK') and not g.event('EVENT_OTHER_SCENE_ACTIVE') and i > 20: break
        if scene == 'sprout' and g.event('EVENT_OTHER_AMBUSH_SPROUT_TOWER') and not g.event('EVENT_OTHER_SCENE_ACTIVE') and i > 20: break
        if scene == 'dragon' and g.event('EVENT_OTHER_AMBUSH_DRAGONS_DEN') and not g.event('EVENT_OTHER_SCENE_ACTIVE') and i > 20: break
        if scene == 'indigo' and g.event('EVENT_OTHER_FINAL_DONE') and not g.event('EVENT_OTHER_SCENE_ACTIVE') and i > 20: break
        if scene == 'home' and i > 40: break
    g.p.tick(90)
    res['bag'] = {str(k): v for k, v in g.bag().items()} if settled(g) else None
    res['party'] = g.party_species() if settled(g) else None
    res['map'] = curmap(g)
    res['flags'] = {n: g.event(n) for n in ('EVENT_OTHER_AMBUSH_NEW_BARK', 'EVENT_OTHER_AMBUSH_SPROUT_TOWER', 'EVENT_OTHER_AMBUSH_DRAGONS_DEN', 'EVENT_OTHER_FINAL_DONE', 'EVENT_OTHER_SCENE_ACTIVE')}
    res['issues'] += [list(i) for i in w.issues]
    res['final_shot'] = shot(g, 'amb_%s_g%s_end' % (scene, gender))
    g.close()
except Exception as e:
    res['error'] = repr(e)[:200] + traceback.format_exc()[-300:]
print('RESULT ' + json.dumps(res, ensure_ascii=True))
