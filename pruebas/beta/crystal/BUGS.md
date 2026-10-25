# Radical Cristal v5.3 - beta test bug list (girl player run: PLAYER_GENDER=1)

Working folder: `C:\Users\xelu3\build\beta\crystal`. All commands are run from that folder. Scripts are in `scripts\`
(`lib.py` is the shared helper, `w_*.py` are single-job workers, `t_*.py` are standalone tests, `prun.py` is the
parallel runner with per-job timeout). Evidence images are in `shots\`, raw results in `logs\`.

Important harness note: the stock harness (`Game(...)`) skips the intro, so the event flags that `InitializeEventsScript`
sets (it hides ~150 NPCs and sets `wVariableSprites`) are NOT set. All my runs use `lib.G`, which injects exactly that
script's `setevent` / `variablesprite` lines at `_InitializeStartDay` (the point where a real new game would already
have them). `NEWSTATE=0` gives the bare stock-harness state.

# STATUS (re-verified on the lead's fixed build, `build\cristal\pokecristal.gbc` copied to `work\source`)

| Bug | Result on the fixed ROM |
|---|---|
| BUG-001 (connections) | **fixed in lead build, verified**: `w_conn.py` over all 68 maps, girl and boy: 0 problems in 127 crossings (`logs/conn_new_g1.jsonl`, `conn_new_g0.jsonl`) |
| BUG-002 (Route 29 dude) | **fixed, verified**: `t_dude_distort.py newbark` 0 garbage frames; `t_dude_paths.py newbark / newbark_menu / newbark_battle`: dude in slot 12 (bank 1), 8 walking-frame tiles used, no problems |
| BUG-003 (other protagonist missing from list) | **fixed, verified** by the same connection scan (Route 27/29 -> New Bark clean for both genders) |
| BUG-004 (stale tiles after fight) | **fixed, verified**: `t_repro_silver.py route29`: Silver tile 24 = list slot 24 before and after, `audit []` |
| BUG-005 (guillemets) | **fixed, verified**: `t_charscan.py` no longer reports SuperLeagueTito |
| BUG-006 (HM moves in random moves) | still open (not part of the lead's list), re-checked by `w_candy.py` logic unchanged |

Regression runs on the fixed ROM, all clean: NPC sweep 1512 objects at 14:00 (0 crash / garbage / hang), fuzz 379 maps (0 issues), 251 moves x 2 sides (0 crash),
menu monkey 75 runs x 4000 inputs (0 crash), lead's `work	est-v45-story.py` girl run 28 PASS, egg hatching 4/4 shiny first-stage.
The REVERSAL / INVERSION crash was never reproduced (see COVERAGE.md).

## Table of contents

| ID | Sev | Title | Status |
|---|---|---|---|
| BUG-001 | wrong behaviour / visual | Crossing a map connection on foot never rebuilds the overworld sprite list: NPCs of the new map are drawn with the player's graphics (or without walk frames) until a warp / battle reloads the map | CONFIRMED; fixed in lead build, verified |
| BUG-002 | visual | Route 29 dude who warns about Ulex (SPRITE_COOLTRAINER_M): when Route 29 is entered from New Bark Town on foot he lives in the standing-only VRAM bank; while he walks UP his OAM uses tiles 156-159 of bank 0 = garbage block (the reported "distortion"), and he never shows walk frames (same root cause as BUG-001) | CONFIRMED; fixed in lead build, verified |
| BUG-004 | visual | After a battle / reloadmap that follows a connection crossing the sprite list is rebuilt but object structs keep their old tile numbers: Silver (Cherrygrove, after the first fight) becomes a black-haired Cooltrainer, the old man becomes another NPC (same root cause) | CONFIRMED; fixed in lead build, verified |
| BUG-006 | wrong behaviour (design) | Random level-up / egg / gift moves can be HM moves (CUT, FLY, SURF, STRENGTH, FLASH, WHIRLPOOL, WATERFALL); the forget menu refuses HM moves, but HMs are now bag tools, so the move is dead weight that cannot be forgotten | CONFIRMED (34 of 251 species after one Rare Candy run) |
| BUG-005 | text | Guillemets in the Super League champion's card text are assembled as raw UTF-8 and print as garbage glyphs | CONFIRMED in ROM bytes; fixed in lead build, verified |
| BUG-003 | visual (gender specific) | The other protagonist (GOLD for a girl, CRISTAL for a boy) is not in the sprite list of New Bark Town when it is entered from Route 27 / 29 on foot, so it would be drawn with the player's own sprite | CONFIRMED; fixed in lead build, verified |

(more entries are appended below as the run continues)

---

## BUG-001 - Map connections do not rebuild the sprite list; NPCs drawn with the player's graphics

* **Severity:** wrong behaviour (visual, but it also makes scripted walkers slide without animation).
* **Status:** CONFIRMED. Reproduced in 20 of the 127 crossings that the harness could perform, with the girl and the boy.
  This is the cause of the "reported but not reproduced" items: *NPCs change their sprite when you leave/come back or
  enter/leave an area, Silver after the first fight in Cherrygrove, NPCs on Route 29 and in Goldenrod drawn with another
  NPC's graphics, Route 29 tutorial dude distorted while walking.*
* **Reproduction (automatic, all connections):**
  `set PLAYER_GENDER=1` then `py -3.12 -W ignore scripts/prun.py scripts/w_conn.py logs/jobs_conn.json logs/conn_g1.jsonl 3 600`
  then `py -3.12 scripts/show_conn.py logs/conn_g1.jsonl` (`PLAYER_GENDER=0` for the boy: `logs/conn_g0.jsonl`).
  The worker (`scripts/w_conn.py MAP_A`) spawns on the edge of map A, walks across every connection into map B and checks
  each object of B: is its sprite id in `wUsedSprites` (`NOSLOT`), does the object's VRAM tile hold the ROM graphics
  (`STAND-GFX-MISMATCH`), is a walking-type sprite parked in the standing-only table (`WALKER-IN-BANK0`).
* **Reproduction (single, with picture):**
  `py -3.12 -W ignore scripts/t_repro_conn.py ROUTE_38 ECRUTEAK_CITY 39 8 right 2 ecruteak`
  prints `audit [('NOSLOT', 1, 'SPRITE_FISHER', ...), ('NOSLOT', 2, 'SPRITE_YOUNGSTER', ...)]` and
  `fullcheck [(1,'SPRITE_FISHER',0,'STAND-GFX-MISMATCH'), (2,'SPRITE_YOUNGSTER',0,...)]` (object struct tile 0 = the player's
  tile) after walking from Route 38 into Ecruteak City, and a clean audit when the same spot is loaded by a warp.
  Pictures: `shots\conn_ecruteak_side_by_side.png` (left: walked in, right: same place loaded by a warp; the two NPCs on the
  left wear the girl player's blue-haired graphics).
* **Expected:** every NPC of the map you walk into has its own graphics (as when you enter by a door).
* **Actual:** the NPC is drawn with the *player's* tile set (object struct tile = `wUsedSprites+1`) or, if its sprite was in the
  old list but past the 10th walking sprite, with the standing-only frames. It becomes right only after something reloads the
  map (door/warp, battle with `reloadmap`, fly, ...), so NPCs seem to "change sprite when you leave and come back".
* **Root cause:** `data/maps/setup_scripts.asm`, `MapSetupScript_Connection` has no `LoadMapGraphics`/`RefreshMapSprites`:
  `LoadMapObjects` creates the new map's object structs (`InitializeVisibleSprites -> GetSpriteVTile`) against the sprite list
  that was built for the previous map (`RefreshSprites`, called only by `LoadMapGraphics` in warp/reload scripts).
  `GetSpriteVTile` (home/map_objects.asm) returns the player's tile (`wUsedSprites + 1`, carry set) for a sprite that is not in the
  list. The vanilla design avoided this by giving every map group the sprites of the whole region; this hack's lists
  (`data/maps/outdoor_sprites.asm`, 23 entries per group, `COPYCAT` instead of `KAREN`) do not cover the neighbouring group
  (e.g. Route 35 is in group VIOLET, Goldenrod City in group GOLDENROD; Route 38 / Ecruteak ...), and with the 10-walker limit of the
  bank-1 table (tiles 0-119 + walk frames at +128) any 11th walking sprite is parked in the standing-only table.
* **Affected crossings (girl run; "missing" = drawn with the player's graphics):**

| From -> To | NPC sprites missing from the list | walker stuck in VRAM bank 0 | note |
|---|---|---|---|
| CINNABAR_ISLAND -> ROUTE_20 | JANINE_IMPERSONATOR, CHRIS | | |
| ECRUTEAK_CITY -> ROUTE_42 | POKEFAN_M | | |
| FUCHSIA_CITY -> ROUTE_19 | SWIMMER_GIRL, SWIMMER_GUY x3 | | |
| GOLDENROD_CITY -> ROUTE_35 | FISHER, BUG_CATCHER, SUPER_NERD | | |
| NEW_BARK_TOWN -> ROUTE_27 | POKE_BALL x2 | | |
| NEW_BARK_TOWN -> ROUTE_29 | FRUIT_TREE, POKE_BALL | COOLTRAINER_M (tutorial dude) | |
| ROUTE_19 -> FUCHSIA_CITY | POKEFAN_M | | |
| ROUTE_20 -> ROUTE_19 | JANINE_IMPERSONATOR | | |
| ROUTE_21 -> PALLET_TOWN | | TEACHER | |
| ROUTE_27 -> NEW_BARK_TOWN | CHRIS (girl) / KRIS (boy) | | other protagonist, see BUG-003 |
| ROUTE_29 -> NEW_BARK_TOWN | CHRIS (girl) / KRIS (boy) | | other protagonist, see BUG-003 |
| ROUTE_3 -> ROUTE_4 | LASS x2 | | |
| ROUTE_31 -> VIOLET_CITY | LASS, SUPER_NERD | | |
| ROUTE_32 -> ROUTE_33 | POKEFAN_M | | |
| ROUTE_33 -> ROUTE_32 | FISHER x4, COOLTRAINER_M, POKE_BALL x2 | | |
| ROUTE_35 -> GOLDENROD_CITY | POKEFAN_M x2, COOLTRAINER_F x2, ROCKET x7 | | the 7 Rockets of the radio-tower takeover |
| ROUTE_38 -> ECRUTEAK_CITY | GRAMPS x3, FISHER, YOUNGSTER | | verified with a picture |
| ROUTE_43 -> MAHOGANY_TOWN | POKEFAN_M | | |
| ROUTE_7 -> SAFFRON_CITY | POKEFAN_M, COOLTRAINER_M, COOLTRAINER_F | | |
| ROUTE_8 -> SAFFRON_CITY | LASS x2, COOLTRAINER_M, COOLTRAINER_F | | |

  (15 further connections could not be crossed by the harness - blocked tiles / cut trees: Violet-Route 31 east, Azalea-Route 34,
  Ecruteak-Route 38/42 west edge, Route 29-46, Route 36-35, Route 17/16/18, Route 15, Route 12, Route 6, Route 5, Saffron-Route 8.
  They are listed as NOCROSS in `logs/conn_g1.jsonl`; they probably share the problem.)
* **Proposed fix (validated on the binary):** make the connection script rebuild the sprite list *before* `LoadMapObjects`
  creates the object structs, i.e. in `MapSetupScript_Connection` use `mapsetup LoadMapGraphics` (it already contains
  `LoadMapTileset`) instead of `mapsetup LoadMapTileset` (or add `mapsetup RefreshSprites`-equivalent right after `LoadMapAttributes`).
  Test: with `FIXCONN=1` the harness patches exactly that one byte in the ROM image
  (`MapSetupScript_Connection`: command `LoadMapTileset` ($0f) -> `LoadMapGraphics` ($0e)):
  `set FIXCONN=1` then the same `prun ... w_conn.py` command gives **0 problems in all 127 crossings** (`logs/conn_fix_g1.jsonl`).
  Alternative/extra hardening: widen the group lists so that bordering groups share their NPC sprites, and do not give
  walking sprites to the standing-only table (e.g. count only real walkers, or reserve the first-table slots for the map's own objects).
* **Also seen:** the list is rebuilt by `ReloadTilesetAndPalettes` (battles, `reloadmap`) but struct tiles of already created
  objects are not recomputed; opening and closing the Start menu does NOT fix it (`scripts/t_repro_menu.py`).

### BUG-001 addendum - what is inherited and what the hack added (comparison with `buildase0`, the Spanish base ROM)

`BASEROOT=C:/Users/xelu3/build/base0 py -3.12 scripts/prun.py scripts/w_conn.py logs/jobs_conn.json logs/conn_base0_g1.jsonl 3 600`
(`logs/conn_base0_g1.jsonl`) and `py -3.12 -W ignore scripts/t_base_compare.py`:

* The base ROM already has the design limitation: 13 of the 127 crossings are affected there (Goldenrod-Route 35 both ways with the 7 Rockets of the takeover,
  Route 38 -> Ecruteak, Route 32/33, Route 31 -> Violet, Route 19/Fuchsia, Route 7/8 -> Saffron, Route 3 -> 4, Ecruteak -> Route 42, Route 43 -> Mahogany).
* **Added by this hack (7 crossings, absent in base0):** New Bark Town <-> Route 29 (dude in bank 0, Route 29 fruit tree and ball missing), New Bark Town <-> Route 27
  (balls), Route 27/29 -> New Bark (CHRIS/KRIS other-protagonist object missing), Cinnabar -> Route 20 / Route 20 -> Route 19 (JANINE_IMPERSONATOR, CHRIS), Route 21 -> Pallet
  (walking Teacher in bank 0). They come from the extra sprites that the hack puts into the lists (always-listed hidden objects `SPRITE_CHRIS`/`SPRITE_KRIS`, the
  `SPRITE_COPYCAT` variable slot that replaced `SPRITE_KAREN`, Joy/Tito/Ulex objects) which push the 11th walking sprite past the 10 that fit in the walk-capable table.
  The Route 29 tutorial-dude distortion therefore is a regression of the hack, not of the base game.

## BUG-002 - Route 29 tutorial dude: no walk animation / stuck in the standing-only bank

* **Severity:** visual. **Status:** CONFIRMED (same cause as BUG-001).
* **Reproduction:** `py -3.12 -W ignore scripts/t_repro_dude.py newbark 8` (girl; add `PLAYER_GENDER=0` for the boy), then compare
  `py -3.12 -W ignore scripts/t_repro_dude3.py newbark` vs `... warp` (sheets `shots\dude_walk_newbark_g1.png`, `shots\dude_walk_warp_g1.png`).
  Walk west from New Bark Town (spawn (0,8)) into Route 29; at (53,8) the dude reacts and walks up 4 and right 2.
* **Expected:** he walks with the two-frame leg animation (control: `warp` mode, OAM tiles 144-151 in bank 1).
* **Actual:** his sprite (COOLTRAINER_M) was placed in tile slot 152 (VRAM bank 0, standing-only, `<=BANK0-standing-only`); while he walks
  the OAM only uses the standing tiles 24-35 of bank 0, so he slides across the screen like a statue (no animation), and a walking
  frame lookup into the second half of that bank is not backed by data. `t_repro_dude2.py newbark` prints the OAM tile statistics.
* **Root cause:** BUG-001 plus the sprite budget of the New Bark list: `AddSpriteGFX` skips list index 0 (the player), so the
  other-protagonist objects of New Bark (`SPRITE_CHRIS` and `SPRITE_KRIS`, always in the list although hidden by event flags)
  duplicate the player's own sprite and waste 12 tiles; the New Bark list holds 11 walking-type sprites, the 11th (the dude) falls into
  bank 0. Listing: `py -3.12 -W ignore scripts/t_repro_dude.py newbark 8`.
* **Proposed fix:** BUG-001 fix (the list is rebuilt for Route 29 with the dude first); additionally skip duplicate of the player's
  sprite id in `AddSpriteGFX` (start the search at `wUsedSprites` instead of `+ 2` for ids equal to the player's) and do not add the
  hidden other-protagonist objects when `EVENT_OTHER_*_HIDDEN` is set.

## BUG-003 - Other protagonist missing from the New Bark Town sprite list when arriving on foot (gender specific)

* **Severity:** visual (gender specific), **Status:** CONFIRMED at list level (`missing_from_list` in `logs/conn_g1.jsonl` / `conn_g0.jsonl`).
* Girl player: object `NEWBARKTOWN_OTHER_BOY` (SPRITE_CHRIS = GOLD) is not in the list when New Bark Town is entered from Route 27 or Route 29;
  boy player: `NEWBARKTOWN_OTHER_GIRL` (SPRITE_KRIS = CRISTAL) is missing. If the ambush (or any scene with the object) runs in that
  state the object is drawn with the player's own sprite (and with the player's walk frames), i.e. GOLD would look like the girl player.
* Same root cause and fix as BUG-001.

### BUG-002 addendum - the actual distortion (coordinator clarification: the NPC is the Route 29 character at (50,12) who now warns about Ulex)

* **Reproduction:** `py -3.12 -W ignore scripts/t_dude_distort.py newbark` (girl; `PLAYER_GENDER=0` boy). Prints
  `frames with garbage OAM tiles (bank 0, tile>=128): 48` and saves `shots\dude_distort_newbark_g1.png`: while the dude takes his first steps
  UP the whole sprite becomes an orange square of text/BG tiles. The control `... t_dude_distort.py warp` (spawn directly on Route 29) gives 0 frames.
  With `FIXCONN=1` also 0 frames.
* **Mechanism:** with the list built for New Bark Town the dude (11th walking-type sprite) gets tile slot 152, i.e. VRAM bank 0 tile $18
  (the standing-only second table). His facing frame is chosen as `slot + 4` = 156 and written to OAM *without masking bit 7*, and the
  attribute selects bank 0, so the hardware draws tiles $9C..$9F of bank 0 = $89C0.. (font/box tiles) instead of his sprite.
  Walking NPCs in that table also never get their walk frames. `scripts/t_dude_paths.py <path>` runs the whole walk after arriving by
  different paths; results (girl): `newbark`, `newbark_menu`, `newbark_bike`, `newbark_surf`, `newbark_battle` all keep the dude in
  slot 152 (menu / bike / surf / a wild battle do NOT repair it, because the list is rebuilt identically for Route 29 only when a warp/Continue
  reloads); `warp`, `gate46` (Route 29-46 gate warp), `cherrygrove` (list from Cherrygrove has him in slot 108, bank 1) and
  Save + soft reset + Continue (`scripts/t_savecontinue.py`) are all clean.
* Only the path New Bark -> Route 29 on foot is affected; the stock lead tests spawned directly on Route 29 (warp-built list) or crossed from Cherrygrove.
* Note for other walkers: every scripted NPC that is parked in the standing-only table will show the same garbage when it walks (e.g. the
  Pallet Town teacher when arriving from Route 21, `mk_conn_table` output above).

## BUG-004 - Stale object tiles after the map is reloaded (Silver and the old man change graphics after the first rival fight)

* **Severity:** visual. **Status:** CONFIRMED, fix validated.
* **Reproduction:** `py -3.12 -W ignore scripts/t_repro_silver.py route29` (girl). Route 29 -> Cherrygrove on foot (spawn Route 29 (0,6), 4 steps left),
  rival scene (`wCherrygroveCitySceneID=1`), fight. Output: `rival struct tile at appear: 108 list says 108` (correct before), then
  `AFTER FIGHT: Silver struct tile 108 but list slot for SPRITE_RIVAL is 24 -> drawn with ['108 SPRITE_COOLTRAINER_M ...']` and
  `audit [('TILE', 1, 'SPRITE_GRAMPS', 'struct=84 list=12')]`. Picture: `shots\silver_after_fight_route29_g1.png` (Silver, red haired, runs away as a black haired Cooltrainer M).
  Control (`warp`): clean. `FIXCONN=1`: clean (`audit []`).
* **Expected:** an NPC keeps its graphics when the map is reloaded after a battle.
* **Actual:** `reloadmap` / `reloadmapafterbattle` run `MapSetupScript_ReloadMap` -> `LoadMapGraphics` -> `RefreshSprites`, which rebuilds the sprite list for
  the current map, but the already created object structs keep the tile numbers they received from the *previous* list. In vanilla the rebuilt
  list is identical to the old one; here it is not after a connection crossing (BUG-001), so every NPC drawn before the fight is now drawn with the graphics
  of whatever sprite occupies its old slot. The same happens with any later reload (trainer battles, wild battles, `reloadmap` scripts).
* **Fix:** BUG-001 fix. Defensive extra: in `RefreshSprites` also refresh `OBJECT_SPRITE_TILE` of every active object struct (call `GetSpriteVTile` again).

## BUG-005 - Super League champion's card: guillemets print as garbage

* **Severity:** text (minor). **Status:** CONFIRMED in the ROM image (bytes `c2 ab` / `c2 bb` at 0x1813c7 and 0x181442 = `U-umlaut`, `l` / `U-umlaut`, `e-grave` glyphs).
* **Where:** `maps/SuperLeagueTito.asm:110` `"«Eres el puto amo,"` and `:117` `"cabra!»"`. `«` and `»` have no charmap entry, so RGBDS emits the UTF-8 bytes C2 AB / C2 BB.
* **Expected:** quote marks. **Actual:** the text shows `Ul` before "Eres el puto amo," and `Ue` after "cabra!".
* **Fix:** use `“` / `”` ($72 / $73 exist in the charmap) or plain `"`-less text; check with `scripts/t_charscan.py` (reports only these two plus the intended `¯` of landmarks).
* Also from the static lint (`scripts/t_textlint.py`): `maps/ElmsLab.asm:1190-1193` has `line ""` followed by `line "que no quieras que"` (empty line, no visible effect) and
  `data/moves/descriptions.asm:284` has a 19 column line (`cuchillas cruzadas.`, one over the 18 columns).

## BUG-006 - Random moves may be HM moves that cannot be forgotten

* **Severity:** wrong behaviour / design (Nuzlocke-relevant: dead move slots). **Status:** CONFIRMED.
* **Reproduction:** `set PLAYER_GENDER=1` then
  `py -3.12 scripts/prun.py scripts/w_candy.py logs/jobs_candy.json logs/candy_g1.jsonl 3 590` (Rare Candy x40 on every species 1-251 from level 5, all badges)
  and count final movesets that contain an HM move id (15 CUT, 19 FLY, 57 SURF, 70 STRENGTH, 127 WATERFALL, 148 FLASH, 250 WHIRLPOOL): 34 of 251 species
  (13 %), e.g. species 44 ends with STRENGTH and WATERFALL, 84 with CUT and FLASH. Single run: `py -3.12 -W ignore scripts/w_candy.py 5 255 40 44`
  (final moves `[70,158,127,229]`; the learn prompt then reads "dejar sitio a CONTONEO?" -> "Los movimientos MO no se pueden olvidar ahora.").
* **Expected:** a random move offered by the level-up/gift generator is a normal move, or an HM move that is on the mon can be forgotten
  (v5 docs: "MO como herramientas ... sin aprender el ataque").
* **Actual:** `ChooseRandomLevelMove` / `ChooseRandomMoveAtDE` (`engine/pokemon/v2_balance.asm`) pick any id 1..NUM_ATTACKS except STRUGGLE and
  known moves, so HM moves are offered; `engine/pokemon/learn.asm:183` (`IsHMMove` -> `MoveCantForgetHMText`) then blocks forgetting them in the
  learn-move menu. Only the Move Deleter (no HM check) can remove them. A mon whose four slots fill with HM moves cannot learn anything else.
* **Fix:** in both generators reject `IsHMMove` ids (loop `.sample` again), or drop the HM check in `learn.asm` because HMs no longer need the move on the mon.
