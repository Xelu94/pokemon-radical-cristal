"""v5.5 changes played in the emulator: the other protagonist runs up from behind the first time the player heads
for Route 29 with a Pokemon, and TMs are never used up. Run twice (PLAYER_GENDER=1 plays a girl)."""
import json
import os
import sys
from pathlib import Path

base = Path('work/test-v43-changes.py').read_text(encoding='utf8')
exec(base[:base.index('# --- Starting inventory')])   # check(), maps, items and Game
sys.path.insert(0, 'work')
from story_helper import StoryMixin, EVENTS


class G(StoryMixin, Game):
    pass


def strong_party(g):
    g.party([150], level=100)
    for stat in ['MaxHP', 'HP', 'Attack', 'Defense', 'Speed', 'SpclAtk', 'SpclDef']:
        g.p.memory[g.a('wPartyMon1' + stat):g.a('wPartyMon1' + stat) + 2] = [3, 231]
    g.p.memory[g.a('wPartyMon1Moves')] = 94
    g.p.memory[g.a('wPartyMon1PP')] = 30
    g.write('wJohtoBadges', 0xff)   # a level-100 Pokemon only obeys with all the badges
    g.write('wKantoBadges', 0xff)
    at = g.a('wPartyMonNicknames')
    g.p.memory[at:at + 11] = [0x8c, 0x84, 0x96, 0x93, 0x96, 0x8e, 0x50, 0, 0, 0, 0]


def quiet(g):
    return g.read('wBattleMode') == 0 and (g.p.memory[0xff70] & 7) in (0, 1)


def mash(g, done, presses=300, every=6):
    for i in range(presses):
        g.press('a', 30, hold=6)
        if i % every == every - 1 and quiet(g) and done():
            g.p.tick(90)
            if quiet(g) and done():
                return True
    return False


def walk_left_until_scene(g, tries=14):
    """Walk west one step at a time; return True once the ambush scene has started (flag set or battle on)."""
    for _ in range(tries):
        g.press('left', 8, hold=8)
        if g.read('wBattleMode') != 0 or (quiet(g) and g.event('EVENT_OTHER_SCENE_ACTIVE')):
            return True
    return False


girl = os.environ.get('PLAYER_GENDER') == '1'
who = 'Gold' if girl else 'Cristal'
for row in (8, 9):
    g = G('NEW_BARK_TOWN', 4, row)
    strong_party(g)
    g.write('wNewBarkTownSceneID', 1)   # the scene after the Teacher has let the player go
    g.p.tick(60)
    started = walk_left_until_scene(g)
    done = mash(g, lambda: g.event('EVENT_OTHER_AMBUSH_NEW_BARK') and not g.event('EVENT_OTHER_SCENE_ACTIVE'))
    g.p.tick(120)
    where = (g.read('wXCoord'), g.read('wYCoord')) if quiet(g) else None
    check('row %d: walking west with a Pokemon makes %s run up from behind, battle, heal the party and give a Max Potion' % (row, who),
          started and done and g.bag().get(items['MAX_POTION'], 0) == 1 and where is not None and where[0] <= 2)
    # it happens once: heading west again starts nothing
    for _ in range(3):
        g.press('right', 8, hold=8)
    for _ in range(4):
        g.press('left', 8, hold=8)
    g.p.tick(120)
    check('row %d: heading west again does not start another battle' % row, g.read('wBattleMode') == 0 and not g.event('EVENT_OTHER_SCENE_ACTIVE'))
    g.close()

g = G('NEW_BARK_TOWN', 4, 8)
g.write('wNewBarkTownSceneID', 1)
g.p.tick(60)
assert g.read('wPartyCount') == 0
for _ in range(5):
    g.press('left', 8, hold=8)
g.p.tick(120)
check('without a Pokemon walking west starts no ambush', not g.event('EVENT_OTHER_AMBUSH_NEW_BARK') and not g.event('EVENT_OTHER_SCENE_ACTIVE'))
g.close()

# --- TMs are not used up -----------------------------------------------------------------------------------
g = Game('ROUTE_31', 21, 14)
g.party([150], level=50)
g.p.memory[g.a('wPartyMon1Moves'):g.a('wPartyMon1Moves') + 4] = [1, 0, 0, 0]
tm = g.a('wTMsHMs')
g.p.memory[tm] = 3
g.press('start', 40)
for button in ['down', 'a', 'left', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a']:
    g.press(button, 40)
g.p.tick(60)
moves = g.mem('wPartyMon1Moves', 4)
check('teaching a TM works and the TM stays in the bag (3 before, 3 after)', moves[1] != 0 and g.p.memory[tm] == 3)
g.close()

report = {'passed': len(tests), 'tests': tests}
Path('work/v55-story-girl-tests.json' if girl else 'work/v55-story-tests.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
