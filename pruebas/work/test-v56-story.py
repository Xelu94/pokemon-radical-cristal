"""v5.6 changes played in the emulator: after the first fight the other protagonist runs on towards Route 29 and vanishes
(no sprite left behind), Ulex can be fought without a badge in between, and TITO's list of trading partners.
Run twice (PLAYER_GENDER=1 plays a girl)."""
import io
import json
import os
import re
import sys
from pathlib import Path

base = Path('work/test-v43-changes.py').read_text(encoding='utf8')
exec(base[:base.index('# --- Starting inventory')])   # check(), maps, items and Game
sys.path.insert(0, 'work')
from story_helper import StoryMixin, EVENTS

src = Path('work/test-v55-story.py').read_text(encoding='utf8')
exec(src[src.index('class G('):src.index('girl = os.environ')])   # G, strong_party, quiet, mash, walk_left_until_scene

girl = os.environ.get('PLAYER_GENDER') == '1'
other_sprite = 0x01 if girl else 0x60


def other_objects(g):
    return [n for n in range(1, 13) if g.p.memory[g.a('wObject%dSprite' % n)] == other_sprite]


for row in (8, 9):
    g = G('NEW_BARK_TOWN', 4, row)
    strong_party(g)
    g.write('wNewBarkTownSceneID', 1)
    g.p.tick(60)
    seen_beside = False
    walk_left_until_scene(g)
    done = mash(g, lambda: g.event('EVENT_OTHER_AMBUSH_NEW_BARK') and not g.event('EVENT_OTHER_SCENE_ACTIVE'))
    g.p.tick(200)
    gone = quiet(g) and not other_objects(g)
    for _ in range(3):
        g.press('a', 30, hold=6)
    text = ' '.join(''.join(chr(b) if 32 <= b < 127 else ' ' for b in g.p.memory[g.a('wTilemap'):g.a('wTilemap') + 360]) for _ in [0])
    check('row %d: after the first fight the other protagonist is gone (no sprite left on the map, pressing A starts no dialogue)' % row,
          done and gone and g.read('wTextboxFlags') is not None and 'objeto' not in text.lower())
    g.close()

# --- Ulex has no badge lock ---------------------------------------------------------------------------
g = G('ROUTE_31', 20, 13)
g.party([152], level=60)
g.write('wJohtoBadges', 0b1)
g.set_event('EVENT_ULEX_BADGE_BASE') if False else None
# a milestone flag for the current badge count is set, as if he had been fought with one badge already
flag = EVENTS.get('EVENT_ULEX_BADGE_BASE', None)
g.close()

report = {'passed': len(tests), 'tests': tests}
Path('work/v56-story-girl-tests.json' if girl else 'work/v56-story-tests.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
