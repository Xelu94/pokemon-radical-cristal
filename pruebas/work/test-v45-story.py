"""v4.5 story and world changes on the real compiled ROM: the Ulex warning, route nurses, Elm's duel,
the other protagonist (three ambushes, the Indigo Plateau fight, her home and the Zurullo trade),
the Super League, Dark Lugia and the data changes (Gold Berries, balls, prices, stones)."""
import io
import json
import os
import re
import sys
from pathlib import Path
from pyboy import PyBoy

base = Path('work/test-v43-changes.py').read_text(encoding='utf8')
exec(base[:base.index('# --- Starting inventory')])   # check(), maps, items and Game
sys.path.insert(0, 'work')
from story_helper import StoryMixin, EVENTS


class G(StoryMixin, Game):
    pass


def strong_party(g, species=150, level=100, nick=True):
    g.party([species], level=level)
    for stat in ['MaxHP', 'HP', 'Attack', 'Defense', 'Speed', 'SpclAtk', 'SpclDef']:
        g.p.memory[g.a('wPartyMon1' + stat):g.a('wPartyMon1' + stat) + 2] = [3, 231]
    g.p.memory[g.a('wPartyMon1Moves')] = 94
    g.p.memory[g.a('wPartyMon1PP')] = 30
    g.write('wJohtoBadges', 0xff)
    g.write('wKantoBadges', 0xff)
    at = g.a('wPartyMonNicknames')
    g.p.memory[at:at + 11] = [0x8c, 0x84, 0x96, 0x93, 0x96, 0x8e, 0x50, 0, 0, 0, 0]


def settled(g, fn, tries=40):
    """Read fn() only while the game is in the overworld and the value has stopped changing."""
    last, same = None, 0
    for _ in range(tries):
        g.p.tick(20)
        if g.read('wBattleMode') != 0:
            same = 0
            continue
        value = fn()
        same = same + 1 if value == last else 0
        last = value
        if same >= 4:
            return value
    return last


def mash(g, done, presses=900, every=6, button='a'):
    for i in range(presses):
        g.press(button, 30, hold=6)
        if i % every == every - 1 and g.read('wBattleMode') == 0 and (g.p.memory[0xff70] & 7) in (0, 1):
            if done():
                g.p.tick(90)
                if g.read('wBattleMode') == 0 and done():
                    return True
    return False


def static_checks():
    root = Path('work/source')
    # Gold Berries instead of apricorns in the trees
    text = (root / 'data/items/fruit_trees.asm').read_text(encoding='utf8')
    check('no tree gives an apricorn any more', 'APRICORN' not in text and text.count('GOLD_BERRY') == 7)
    # balls
    offenders = []
    for path in (root / 'maps').glob('*.asm'):
        for n, line in enumerate(path.read_text(encoding='utf8').splitlines(), 1):
            if re.match(r'\s(?:itemball|hiddenitem|verbosegiveitem|verbosegiveitemvar|giveitem) (?!MASTER_BALL)\w*(?:POKE_BALL|GREAT_BALL|ULTRA_BALL|LEVEL_BALL|LURE_BALL|MOON_BALL|FRIEND_BALL|FAST_BALL|HEAVY_BALL|LOVE_BALL|PARK_BALL)\b', line):
                offenders.append((path.name, n))
    check('no map places or gives any ball other than the Master Ball', not offenders)
    # prices
    attrs = (root / 'data/items/attributes.asm').read_text(encoding='utf8')
    zero = [label for label in ['ITEM_19', 'RARE_CANDY', 'ITEM_2D', 'ITEM_32', 'ITEM_5A', 'LEFTOVERS', 'MASTER_BALL']
            if re.search(r'; %s\n\titem_attribute 0,' % label, attrs)]
    check('Master Ball, Rare Candy and the five starting combat items are worth 0', len(zero) == 7)
    # Elm's duel has a class (and picture) of its own
    lab = (root / 'maps/ElmsLab.asm').read_text(encoding='utf8')
    classes = (root / 'data/trainers/class_names.asm').read_text(encoding='utf8')
    check('Elm duels as his own trainer class with his own picture, not as Oak',
          'loadtrainer ELM_PROF, ELM_PROF1' in lab and 'dba_pic ElmPic' in (root / 'data/trainers/pic_pointers.asm').read_text(encoding='utf8')
          and (root / 'gfx/trainers/elm.png').exists() and classes.rstrip().endswith('assert_list_length NUM_TRAINER_CLASSES'))
    # Dark Lugia
    lugia = (root / 'data/pokemon/base_stats/dark_lugia.asm').read_text(encoding='utf8')
    check('Dark Lugia is Dark/Flying with Hp 106, Atk 130, Def 90, Spd 110, SpA 154 and SpD 90',
          'db 106, 130,  90, 110, 154,  90' in lugia and 'db DARK, FLYING' in lugia)


static_checks()

# --- The tutorial NPC warns about Ulex ------------------------------------------------------------------
g = G('ROUTE_29', 55, 9)
g.write('wRoute29SceneID', 1)
g.texts(['Route29UlexWarningText'])
g.party([152], level=6)
g.p.tick(30)
for _ in range(3):
    g.press('left', 10, hold=16)
for _ in range(30):
    g.press('a', 30, hold=6)
g.p.tick(60)
print('dude', g.counts, g.event('EVENT_LEARNED_TO_CATCH_POKEMON'), flush=True)
check('walking past the tutorial NPC makes him warn about Ulex and the level 15 rule',
      g.counts['Route29UlexWarningText'] >= 1 and g.event('EVENT_LEARNED_TO_CATCH_POKEMON'))
g.close()

# --- Nurse Joy on a route heals the party ----------------------------------------------------------------
g = G('ROUTE_13', 13, 14)
g.party([152], level=30)
stride = g.a('wPartyMon2') - g.a('wPartyMon1')
g.p.memory[g.a('wPartyMon1HP'):g.a('wPartyMon1HP') + 2] = [0, 3]
g.p.tick(30)
g.press('up', 20, hold=16)
g.press('up', 20, hold=16)
for i in range(30):
    g.press('a', 40, hold=6)
hp = settled(g, lambda: (g.p.memory[g.a('wPartyMon1HP')] * 256 + g.p.memory[g.a('wPartyMon1HP') + 1], g.p.memory[g.a('wPartyMon1MaxHP')] * 256 + g.p.memory[g.a('wPartyMon1MaxHP') + 1]))
check('the nurse on Route 13 heals the party', hp[0] == hp[1] and hp[1] > 3)
g.close()

# --- Ordinary rival sprites keep their walking frames in Cherrygrove ------------------------------------
g = G('CHERRYGROVE_CITY', 35, 7)
g.p.tick(60)
used = list(g.p.memory[g.a('wUsedSprites'):g.a('wUsedSprites') + 64])
slots = {used[i]: used[i + 1] for i in range(0, 64, 2) if used[i]}
check('the rival sprite is loaded in a walking-capable slot in Cherrygrove', slots.get(4, 255) < 128)
g.close()

# --- Elm's duel --------------------------------------------------------------------------------------------
g = G('NEW_BARK_TOWN', 6, 4)
strong_party(g)
g.write('wElmsLabSceneID', 2)
for _ in range(12):
    g.press('up', 8, hold=14)
g.press('right', 20, hold=16)
done = mash(g, lambda: g.event('EVENT_ELM_DUEL_DONE'), presses=700)
species = settled(g, lambda: tuple(g.party_species()))
shiny = settled(g, lambda: tuple(g.is_shiny(i) for i in range(len(g.party_species()))))
print('elm', done, species, shiny, flush=True)
check('beating Elm gives Feraligatr, Meganium and Typhlosion, all shiny', done and species == (150, 160, 154, 157) and shiny == (False, True, True, True))
check('the duel is exhibition: nothing died and the flags are clear',
      not g.event('EVENT_EXHIBITION_BATTLE') and not g.event('EVENT_FORCE_SHINY_GIFT') and g.mem('wPartyMon1HP', 2) != [0, 0])
g.close()

# --- Other protagonist: New Bark ambush -----------------------------------------------------------------
g = G('NEW_BARK_TOWN', 4, 2)
strong_party(g)
g.p.tick(30)
g.press('left', 20, hold=16)
done = mash(g, lambda: g.event('EVENT_OTHER_AMBUSH_NEW_BARK') and not g.event('EVENT_OTHER_SCENE_ACTIVE'), presses=260)
bag = settled(g, g.bag)
check('after the rival leaves New Bark Town the other protagonist battles, heals the party and hands over a Max Potion',
      done and bag.get(items['MAX_POTION'], 0) == 1)
g.close()

# --- Other protagonist: talking to the rival before getting a Pokemon must not start the ambush -----
g = G('NEW_BARK_TOWN', 4, 2)
g.p.tick(60)
assert g.read('wPartyCount') == 0
g.press('left', 20, hold=16)
for i in range(70):
    g.press('a', 30, hold=6)
g.p.tick(60)
check('without a Pokemon the rival shoves you but the other protagonist does not ambush',
      not g.event('EVENT_OTHER_AMBUSH_NEW_BARK') and not g.event('EVENT_OTHER_SCENE_ACTIVE') and g.bag().get(items['MAX_POTION'], 0) == 0)
g.close()

# --- Other protagonist: she stands next to the player and the sprite tiles survive the battle ----------
g = G('NEW_BARK_TOWN', 4, 2)
strong_party(g)
g.p.tick(30)
g.press('left', 20, hold=16)
adjacent = tiles_before = tiles_after = None
for i in range(200):
    g.press('a', 30, hold=6)
    text = ' '.join(g.screen_text())
    if adjacent is None and 'culito' in text:
        # NEWBARKTOWN_OTHER_BOY / _GIRL are script objects 5 / 6 (map objects 4 / 5); a girl player meets Gold
        base = g.a('wMapObjects') + (4 if g.read('wPlayerGender') else 5) * 16
        girl = (g.p.memory[base + 3] - 4, g.p.memory[base + 2] - 4)
        me = g.pos()
        adjacent = abs(girl[0] - me[0]) + abs(girl[1] - me[1]) == 1
        tiles_before = bytes(g.p.memory[1, 0x8000:0x8000 + 16 * 12])
    if tiles_before and 'Bah' in text:
        tiles_after = bytes(g.p.memory[1, 0x8000:0x8000 + 16 * 12])
        break
check('the other protagonist is placed on the tile in front of the player, not at her map spot', adjacent is True)
check('the player walking sprite tiles are not overwritten after the ambush battle', tiles_after is not None and tiles_after == tiles_before)
g.close()

# --- A refused battle (Nuzlocke run over) is a loss: no badge, no stale result, a clean whiteout ---------
g = G('VIOLET_GYM', 5, 3)
g.party([129], level=5)
at = g.a('wPartyMonNicknames')
g.p.memory[at:at + 11] = [0x8c, 0x80, 0x86, 0x88, 0x8a, 0x80, 0x91, 0x8f, 0x50, 0, 0]
g.p.memory[g.a('wPlayerName'):g.a('wPlayerName') + 5] = [0x93, 0x88, 0x93, 0x8e, 0x50]
g.write('wNuzlockeRunEnded', 1)
g.write('wBattleResult', 0)  # the last battle was won: a refused one must still not count as a win
g.p.tick(60)
g.press('up', 20, hold=16)
g.press('up', 20, hold=16)
seen_text = False
for i in range(80):
    g.press('a', 25, hold=6)
    seen_text = seen_text or 'NUEVA' in ' '.join(g.screen_text())
g.p.tick(300)
where = settled(g, g.pos)  # the whiteout warps to the spawn point, which the test sets at (5, 3)
check('with the run over a gym leader refuses to fight, gives no badge and the whiteout shows the Nuzlocke message',
      seen_text and not g.event('EVENT_BEAT_FALKNER') and not g.event('EVENT_BATTLE_REFUSED') and where == (5, 3))
g.close()

# --- Variable sprites: Route 36's tree is drawn as Sudowoodo even if no script set it ----------------------
g = G('ROUTE_36', 34, 9)
g.p.tick(90)
check('Route 36 sets the weird tree to Sudowoodo before the fight, whatever the game skipped',
      g.p.memory[g.a('wVariableSprites') + 4] == 0x52)  # SPRITE_SUDOWOODO
g.close()

# --- The Super League texts of Ulex and Tito are read from their own map bank (no reset) -------------------
def lose_in_super_league(room, x, y, ups, face, word, face2=None):
    g = G(room, x, y)
    g.party([129], level=5)
    at = g.a('wPartyMonNicknames')
    g.p.memory[at:at + 11] = [0x8c, 0x80, 0x86, 0x88, 0x8a, 0x80, 0x91, 0x8f, 0x50, 0, 0]
    g.p.memory[g.a('wPlayerName'):g.a('wPlayerName') + 5] = [0x93, 0x88, 0x93, 0x8e, 0x50]
    g.write('wJohtoBadges', 0xff)
    g.write('wKantoBadges', 0xff)
    g.set_event('EVENT_BEAT_TITO_XELUIS')
    g.set_event('EVENT_SUPER_LEAGUE_RESTORES_GIVEN')
    g.p.tick(30)
    for _ in range(ups):
        g.press('up', 8, hold=14)
    g.press(face, 8, hold=14)
    if face2:
        g.press(face2, 8, hold=14)
    seen = reset = False
    for i in range(500):
        g.press('a', 25, hold=6)
        text = ' '.join(g.screen_text())
        if 'cartucho' in text:
            reset = True
            break
        seen = seen or word in text
    where = settled(g, g.pos)
    g.close()
    return seen and not reset and where == (6, 10)


check('losing to Ulex in the Super League shows his loss text and sends you back to the Pokemon Center',
      lose_in_super_league('SUPER_LEAGUE_ULEX', 4, 16, 9, 'right', 'ahora'))
check('losing to Tito in the Super League shows his loss text and sends you back to the Pokemon Center',
      lose_in_super_league('SUPER_LEAGUE_TITO', 4, 22, 18, 'right', 'calle', 'up'))

# --- The guard in front of Red steps aside once he lets you pass -----------------------------------------
g = G('SILVER_CAVE_ROOM_3', 10, 32)
g.write('wJohtoBadges', 0xff)
g.write('wKantoBadges', 0xff)
g.p.tick(60)
g.press('up', 8, hold=14)
for i in range(30):
    g.press('a', 25, hold=6)
g.p.tick(60)
check('the Silver Cave guard disappears for good after allowing the player to pass', g.event('EVENT_SILVER_CAVE_GUARD_GONE'))
g.close()

# --- The sandbox travel to the League no longer drops the player inside the wall ---------------------------
g = G('INDIGO_PLATEAU_POKECENTER_1F', 6, 10)
g.p.tick(60)
start = g.pos()
g.press('up', 20, hold=16)
g.p.tick(20)
check('the Indigo Plateau sandbox spawn tile is walkable', g.pos() != start)
g.close()

# --- Other protagonist: Sprout Tower ambush -----------------------------------------------------------
g = G('SPROUT_TOWER_3F', 11, 10)
strong_party(g)
g.p.tick(30)
g.p.button_press('up'); g.p.tick(16); g.p.button_release('up')
done = mash(g, lambda: g.event('EVENT_OTHER_AMBUSH_SPROUT_TOWER') and not g.event('EVENT_OTHER_SCENE_ACTIVE'), presses=420)
bag = settled(g, g.bag)
check('in Sprout Tower the other protagonist appears after the rival and gives a Max Potion', done and bag.get(items['MAX_POTION'], 0) == 1)
g.close()

# --- Other protagonist: the fight at the Indigo Plateau Pokemon Center ---------------------------------------
g = G('INDIGO_PLATEAU_POKECENTER_1F', 5, 13)
strong_party(g)
g.p.tick(30)
g.p.button_press('up'); g.p.tick(18); g.p.button_release('up')
done = mash(g, lambda: g.event('EVENT_OTHER_FINAL_DONE') and not g.event('EVENT_OTHER_SCENE_ACTIVE'), presses=900)
party = settled(g, lambda: tuple(g.party_species()))
check('the Indigo Plateau fight ends with an egg in the party and the other protagonist gone for good',
      done and party[-1] == 253 and g.event('EVENT_OTHER_FINAL_DONE'))
g.close()

# --- Her home and the Zurullo trade -----------------------------------------------------------------------
g = G('NEW_BARK_TOWN', 3, 10)
strong_party(g)
g.party([150, 19], level=5)
g.p.memory[g.a('wPartyMon2ID'):g.a('wPartyMon2ID') + 2] = [0xbe, 0xef]
at = g.a('wPartyMonNicknames') + 11
g.p.memory[at:at + 11] = [0x99, 0x94, 0x91, 0x94, 0x8b, 0x8b, 0x8e, 0x50, 0, 0, 0]
g.set_event('EVENT_OTHER_FINAL_DONE')
g.write('wJohtoBadges', 0xff)
g.p.tick(30)
g.press('down', 40, hold=20)
g.p.tick(60)
g.press('up', 12, hold=14)
g.press('right', 12, hold=14)
g.press('up', 12, hold=14)
for _ in range(14):
    g.press('a', 30, hold=6)
party = settled(g, lambda: tuple(g.party_species()))
levels = settled(g, lambda: tuple(g.p.memory[g.a('wPartyMon1Level') + stride * i] for i in range(len(g.party_species()))))
parents_ok = party[0] == 150 and len(party) == 2 and party[1] not in (19, 20, 150)
check('at home she trades a Zurullo for a random third-stage Pokemon at the level cap minus five', parents_ok and levels[1] == 60)
g.close()

# --- Super League: lobby, Azul's room, the defeat rule and the champion reward ----------------------------
g = G('SUPER_LEAGUE_LOBBY', 5, 16)
strong_party(g)
g.set_event('EVENT_BEAT_TITO_XELUIS')
g.p.tick(30)
for _ in range(5):
    g.press('up', 8, hold=14)
for i in range(40):
    g.press('a', 30, hold=6)
    if i > 12 and g.event('EVENT_SUPER_LEAGUE_RESTORES_GIVEN') and g.bag().get(14) == 99:
        break
for _ in range(12):
    g.press('b', 30, hold=6)
check('the Super League official hands over 99 Full Restores and opens the door',
      settled(g, g.bag).get(14) == 99 and settled(g, lambda: g.event('EVENT_SUPER_LEAGUE_RESTORES_GIVEN')))
g.press('left', 8, hold=14)
for _ in range(11):
    g.press('up', 8, hold=14)
g.p.tick(120)
check('the lobby door leads to Azul\'s room', settled(g, lambda: (g.read('wMapGroup'), g.read('wMapNumber'))) == (16, 10))
g.close()

g = G('SUPER_LEAGUE_AZUL', 4, 16)
strong_party(g)
g.set_event('EVENT_BEAT_TITO_XELUIS')
g.set_event('EVENT_SUPER_LEAGUE_RESTORES_GIVEN')
g.p.tick(30)
for _ in range(8):
    g.press('up', 8, hold=14)
g.press('right', 8, hold=14)
g.press('up', 8, hold=14)
won = mash(g, lambda: g.event('EVENT_SUPER_BEAT_AZUL'), presses=2200)
check('beating Azul in the Super League opens his door and leaves no one dead',
      won and not g.event('EVENT_EXHIBITION_BATTLE') and g.mem('wPartyMon1HP', 2) != [0, 0])
g.close()

g = G('SUPER_LEAGUE_AZUL', 4, 16)
g.party([19], level=5)
g.write('wJohtoBadges', 0xff)
at = g.a('wPartyMonNicknames')
g.p.memory[at:at + 11] = [0x8c, 0x84, 0x96, 0x93, 0x96, 0x8e, 0x50, 0, 0, 0, 0]
g.write('wNumItems', 1)
g.p.memory[g.a('wItems'):g.a('wItems') + 3] = [14, 99, 255]
g.set_event('EVENT_BEAT_TITO_XELUIS')
g.set_event('EVENT_SUPER_LEAGUE_RESTORES_GIVEN')
g.p.tick(30)
for _ in range(8):
    g.press('up', 8, hold=14)
g.press('right', 8, hold=14)
g.press('up', 8, hold=14)
lost = mash(g, lambda: g.event('EVENT_SUPER_LEAGUE_LOST'), presses=700)
check('losing in the Super League returns to the Pokemon Center, takes the Full Restores, keeps the Pokemon and locks the league',
      lost and settled(g, g.bag).get(14, 0) == 0 and settled(g, lambda: g.party_species()) == [19]
      and settled(g, lambda: (g.read('wMapGroup'), g.read('wMapNumber'))) == (16, 2)
      and not g.event('EVENT_SUPER_LEAGUE_RESTORES_GIVEN') and not g.event('EVENT_SUPER_BEAT_AZUL'))
g.close()

g = G('SUPER_LEAGUE_TITO', 4, 22)
strong_party(g)
g.set_event('EVENT_BEAT_TITO_XELUIS')
g.set_event('EVENT_SUPER_BEAT_TITO_ROOM')   # shortcut past the 6 legendaries: the battle itself is covered by Azul's room
g.p.tick(30)
for _ in range(24):
    g.press('up', 6, hold=14)
    if g.pos()[1] <= 5:
        break
g.press('right', 8, hold=14)
g.press('up', 8, hold=14)
mash(g, lambda: g.event('EVENT_SUPER_LEAGUE_BEAT_TITO'), presses=300)
species = settled(g, lambda: tuple(g.party_species()))
shiny = settled(g, lambda: tuple(g.is_shiny(i) for i in range(len(g.party_species()))))
mail = settled(g, lambda: g.p.memory[g.a('wPartyMon1Item') + stride])
check('the Super League champion hands over a shiny level-100 Charizard holding a letter',
      species == (150, 6) and shiny[1] and mail == 158)
g.close()

report = {'passed': len(tests), 'tests': tests}
Path('work/v45-story-girl-tests.json' if os.environ.get('PLAYER_GENDER') == '1' else 'work/v45-story-tests.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
