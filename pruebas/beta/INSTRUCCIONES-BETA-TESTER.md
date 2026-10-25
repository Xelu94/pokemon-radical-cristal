# Beta tester brief — Radical Cristal (GBC ROM hack, v5.3)

You are a **beta tester**. Your job is to play the game in an emulator harness, as thoroughly and adversarially as
you can, and to **find and document bugs**. You do NOT fix the ROM source (the lead engineer does that); you
produce reproducible bug reports and, where you can, a precise root-cause guess and a proposed fix.

## What the project is
"Radical Cristal — Tito Xeluis": a Spanish Pokémon Crystal ROM hack (SM83 assembly, RGBDS 1.0.0, pokecristal base)
with a built-in Nuzlocke, level caps, a physical/special split, Tito Xeluis (NPC), Ulex the thief, the other
protagonist (GOLD or CRISTAL) who ambushes the player, Elm's duel, a "Super League" at level 100 after beating Tito,
Dark Lugia (species 252), Joy nurses on routes, evolution stones in shops, etc. Docs: `C:\Users\xelu3\Desktop\PROYECTO POKEMON CRISTAL NUCKLOCKE\Material-GitHub-Cristal-v4.2\REPOSITORIO\pokemon-cristal-nuzlocke\`
(README.md, CHANGELOG.md, docs/*.md — read CHANGELOG.md and docs/MECANICAS.md, docs/SUPERLIGA-Y-RIVAL.md first).
Source tree (READ ONLY for you): `C:\Users\xelu3\build\cristal` (maps/*.asm hold the scripts and objects, engine/, data/).

## Rules
* **Never edit** `C:\Users\xelu3\build\cristal`, the repository, or anything under `C:\Users\xelu3\Desktop`.
  Work only inside your own folder (given in your task). Copy what you need there first.
* Use at most **3 parallel Python processes** (another tester runs at the same time).
* Run Python as `py -3.12 -W ignore script.py` from the harness root (`...\testroot`-like folder you copy).
  Pipe output through `grep -v INFO`. Always add `faulthandler.dump_traceback_later(N, exit=True)` so a hung
  emulator cannot block you; keep each command under 10 minutes.
* The game is long. Work in stages, save scripts and logs in your folder, and keep a running `BUGS.md`.
  Do not stop at the first bug: keep going and collect many.

## The harness (PyBoy 2.8.1, headless)
Copy `C:\Users\xelu3\build\testroot\work` to `<your folder>\work` and the ROM files
`C:\Users\xelu3\build\cristal\pokecristal.gbc`, `pokecristal.sym`, `pokecristal_debug.gbc`, `pokecristal_debug.sym` to
`<your folder>\work\source\` (the harness reads `work/source/pokecristal.gbc`; the `constants/` and `data/` folders it
parses are also needed in `work/source/`: copy `C:\Users\xelu3\build\cristal\constants`, `data`, `maps`, `engine` there).
Run scripts with the current directory = `<your folder>` so `work/...` paths resolve.
Typical prologue (see `work/cap-v5.py`, `work/test-v45-story.py`, `work/sl-loss.py` for many examples):

```python
import sys, os
from pathlib import Path
base = Path('work/test-v43-changes.py').read_text(encoding='utf8')
exec(base[:base.index('# --- Starting inventory')])      # defines Game, maps, items, root
sys.path.insert(0, 'work')
from story_helper import StoryMixin, EVENTS               # EVENTS = event flag name -> number
class G(StoryMixin, Game): pass
g = G('NEW_BARK_TOWN', 4, 2)         # spawns the player at map constant + (x, y); intro skipped
g.party([152], level=100)            # species ids (decimal), see constants/pokemon_constants.asm
g.set_event('EVENT_BEAT_TITO_XELUIS'); g.event('EVENT_X')   # event flags
g.write('wJohtoBadges', 0xff); g.write('wKantoBadges', 0xff)
g.press('a', 25, hold=6)             # button, frames after, frames held
g.p.tick(60); g.p.screen.image       # PyBoy instance; PIL screenshot
g.screen_text()                      # text rows on screen (accents are dropped by the font mapping)
g.pos(); g.read('wMapNumber'); g.mem('wMapGroup', 2); g.a('wPartyMon1Level'); g.bag()
```
* `PLAYER_GENDER=1` (environment variable) makes the player a **girl** (Crystal/Cristal); default is a boy (Gold).
  The other protagonist ambushing the player is the *other* gender.
* The intro (Oak speech) is skipped; many NPC scripts depend on event flags/scene variables (`wXxxSceneID`) —
  set them with `g.set_event(...)` / `g.write(...)` to replay the story state you need. Symbols come from
  `pokecristal.sym` (`g.symbols`). Event flag names are in `constants/event_flags.asm`.
* **WRAM reads during battle/transitions are bank-switched garbage.** Only trust reads when
  `g.read('wBattleMode') == 0 and (g.p.memory[0xff70] & 7) in (0, 1)` (see `mash()` in `work/test-v45-story.py`).
* A "strong party" helper (a level-100 Mewtwo with huge stats) is in `work/cap-v5.py` (`strong_party`).
  Give party Pokémon a nickname (see that file) or text printing garbles.
* **Crash detection**: the game resets to a boot screen with the text "Este cartucho está diseñado para ser usado
  únicamente en Game Boy Color" (visible as 'cartucho' in `screen_text()`); a hung loop shows the same PC forever.
  You can also `g.p.hook_register(0, 0x0100, callback, ctx)` to catch a reset. 
* Sprite checks: `work/vramcheck.py` (`verify(g, label)` compares sprite graphics in VRAM with the ROM data for the
  sprite list), `work/sprite-consistency.py`, `work/transitions.py` (walks through every building door),
  `work/vram-all.py` (all maps at spawn), `work/connections.py`. Mon overworld sprites (id >= 0x80) are skipped.
* Other helpers: `work/slots.py` (sprite slot list for a map), `work/ulex-loop2.py` (Super League fights),
  `work/walk-rooms.py`, `work/whiteout-*.py`, `C:\Users\xelu3\build\smoke_maps.py` (`catalog()` = every map with a
  safe spawn tile). Known false positives: elevators, link/trade rooms and `COPYCATS_HOUSE_2F` hang the emulator
  (also in vanilla); dark caves look all black without Flash; scenes that trigger on arrival (e.g. Bill in the
  Ecruteak Pokémon Center) hold the player for a few seconds.
* Sandbox ROM (`pokecristal_debug.gbc`): Start menu has a SANDBOX entry (Viajar, Subir medallas, Liga/Rojo,
  Equipo de prueba, Reiniciar retos, Objetos, Opciones). Normal ROM: no sandbox.

## What to do
Play the whole game **in story order** (Johto first: New Bark → Cherrygrove → Violet → Azalea → Goldenrod →
Ecruteak → Olivine → Cianwood → Mahogany → Blackthorn → League; then Kanto and Mt. Silver; then the post-game:
Tito, Super League, Dark Lugia). At every map:
1. Talk to **every NPC / object / sign / item ball / bg event** (parse `object_event`/`bg_event` lines in
   `maps/<Map>.asm`). Read the dialogue to the end; flag text that is cut off, overflows a line, shows garbage
   characters, repeats wrongly, talks about the wrong person, or hangs.
2. Check **sprites**: NPCs keep the same sprite before and after you leave and come back, enter/exit buildings,
   cross map connections, fight a battle, open menus (bag, party, summary, Pokédex), use Fly/Teleport, use the sandbox
   travel, reload a save; sprites animate correctly when they walk or spin (no distortion). Compare screenshots
   of the same NPC taken at different times and run the VRAM checks.
3. Fight **every trainer** (use a strong party so battles end) and check: no crash/hang, correct trainer picture
   and class name, win/loss texts, rewards, post-battle scripts, the Nuzlocke rules (deaths marked, whiteout and
   "run ended" message), level caps, Ulex (roaming thief) encounters, Tito, the other protagonist's four ambushes
   (New Bark, Sprout Tower, Dragon's Den, Indigo Plateau) + her home, Elm's duel, the Super League rooms (Azul,
   Lance, Rojo, Ulex, Tito) winning and losing.
4. **Force other possibilities**: both genders, all times of day (`wTimeOfDay`) and weekdays, party full / empty /
   all fainted / all dead, bag full, PC boxes full, missing or already-set event flags (as the sandbox leaves them),
   skipping optional events, repeating one-time events, trading, breeding (10-step shiny eggs), evolutions
   (levels, stones, trade, happiness), every item's use, every move used by the player and by the enemy
   (a move named INVERSIÓN = REVERSAL, id 179, was reported to crash the game; also test FLAIL and all 251 moves),
   Rare Candies (new quantity selector, 1-99 at once), shops (every mart: evolution stones are sold in the general
   marts from Goldenrod on), Joy nurses, Pokédex (all three sort modes, Dark Lugia 252), PC, Pokégear.
5. Known already-fixed issues you should *regression-test* (see CHANGELOG): sprite tile corruption after battles,
   other protagonist placed far away, refused-battle whiteout text displaced, Ulex/Tito Super League text-bank crash,
   Elm using Oak's picture, shiny gifts going to the PC, Sudowoodo sprite, Silver Cave guard. Currently
   **reported but not yet reproduced**: NPCs changing sprite when you leave and come back to a map or enter/leave an
   area (e.g. Silver after the first fight in Cherrygrove; NPCs on Route 29 and in Goldenrod drawn with another
   NPC's graphics), the Route 29 tutorial dude's sprite distorting while he walks, and the REVERSAL crash.
   Reproducing these is your top priority.

## Deliverables (in your folder)
* `BUGS.md` — for each bug: ID, title, severity (crash / wrong behaviour / visual / text / minor), exact
  **reproduction** (the script path + arguments, or step list with map, coordinates, flags, party), expected vs
  actual, evidence (screenshot path, VRAM check output), suspected **root cause** (file and label in the source) and a
  **proposed fix**. Keep a short table of contents at the top. Mark each bug CONFIRMED (reproduced twice) or
  SUSPECTED.
* `COVERAGE.md` — what you covered (maps, NPCs, trainers, moves, items) and what you could not, and why.
* All scripts you wrote, under `<your folder>\scripts\`, runnable as documented.
* Final answer (returned to the lead): the number of bugs by severity, the top 10 with one line each, and the
  paths of the files above.
