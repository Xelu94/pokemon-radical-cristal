# BUGS.md — Radical Cristal v5.3, beta test as GOLD (boy)

Tester: GOLD run. ROM: `pokecristal.gbc` from `C:\Users\xelu3\build\cristal` (normal) and `pokecristal_debug.gbc`.
Harness: PyBoy 2.8.1 headless, scripts in `C:\Users\xelu3\build\beta\gold\scripts\` (run from `C:\Users\xelu3\build\beta\gold`
with `py -3.12 -W ignore scripts\<name>.py ...`). Screenshots are in `shots\`, raw scan logs in `logs\`.

**Important methodological note.** The stock harness (`work/test-v43-changes.py`) skips the new-game script
(`InitializeEventsScript`), so ~100 "hidden" NPCs are visible and `wVariableSprites` is all zero. `scripts/lib.py` replays
that script just before the first map loads (class `G`), exactly as the real New Game does, and can set the clock
(`G(..., hour=, weekday=)`). All scans below use that state. The stock state was also tried (`NEWGAME=0`) where it matters.

Status legend: CONFIRMED = reproduced at least twice (different scripts / different maps); SUSPECTED = one observation or code reading only.

## Table of contents

| ID | Severity | Status | One line |
|---|---|---|---|
| BUG-001 | visual (very frequent) | CONFIRMED | After crossing any map connection, the next sprite refresh (menu, battle) draws NPCs with another NPC's graphics (Silver/Guide Gent in Cherrygrove, the New Bark teacher...) |
| BUG-002 | visual (every new game) | CONFIRMED | Arriving on foot from New Bark, the Route 29 Ulex-warning dude is drawn with background tiles while he walks; other connections leave objects with no graphics slot (drawn as the player) |
| BUG-003 | **crash** | CONFIRMED | Choosing a move other than the locked one while holding Banda/Gafas/Pañuelo Elegidos prints the lock text from the wrong ROM bank and resets the console (probably the reported INVERSIÓN crash) |

Totals: 1 crash, 0 wrong behaviour, 2 visual, 0 text, 0 minor. Not reproduced: REVERSAL itself (it is fine; see BUG-003), door/stair/cave warps (clean), save+continue (clean).

### Other observations (not bugs / harness notes)
* Interactive scripts (marts, Tito's menu, PC, ruins puzzles, Academy blackboard) never end under button mashing: expected.
* `Evento de objeto.` is printed when talking to the placeholder objects of the other protagonist / Silver (`ObjectEvent` scripts); they are hidden in normal play, so it is only reachable through a state that shows them.
* The other protagonist's battle banner reads "CRISTAL RIVAL quiere luchar" (trainer class RIVAL by design, docs/SUPERLIGA-Y-RIVAL.md).
* Stock-harness caveat: `work/test-v43-changes.py` skips `InitializeEventsScript`; sprite/NPC tests should use `scripts/lib.py` `G` or add that script, otherwise ~100 NPCs that should be hidden are visible and `wVariableSprites` is 0.
* RTC in the harness always starts at hour 0 (night) unless `set_clock`/`G(hour=...)` is used; every earlier test therefore ran at night only.


---

## BUG-001 — NPCs get another NPC's graphics after crossing a map connection and then opening a menu / fighting (the "sprite changes when leaving/returning" report)

* **Severity:** visual (very frequent; affects every route/town border)
* **Status:** CONFIRMED (3 independent reproductions: connection scan, New Bark teacher, Cherrygrove/Silver scene)
* **Reported symptoms it explains:** "NPCs change sprite when you leave/return to a map or enter/leave an area", "Silver changes
  sprite after the first fight in Cherrygrove", "NPCs on Route 29 / Goldenrod drawn with another NPC's graphics".
* **Reproduction (shortest):** `py -3.12 -W ignore scripts\repro_bug001.py`
  1. New game state, party of 1, spawn `ROUTE_29` (57, 9), walk right until the map becomes `NEW_BARK_TOWN`.
  2. Open the bag and close it (Start -> MOCHILA -> B -> B): this is `CloseSubmenu -> ReloadTilesetAndPalettes -> RefreshSprites`.
  3. Walk to the Teacher at (6, 8) (she is created at the border).
  * Expected: the black-haired teacher. Actual: she is drawn with SILVER's sprite (red hair). Screenshot:
    `shots\BUG001_side_by_side.png` (left = control without the bag, right = bug).
  * Same effect in the exact reported scene: `py -3.12 -W ignore scripts\repro_silver.py` (Route 29 -> Cherrygrove on foot, trigger Silver's
    first battle at (33,6)): after `reloadmap` Silver *and* the Guide Gent are drawn with other NPCs' tiles
    (`STALE_TILE struct 2 SPRITE_RIVAL tile 108 != slot 24`), control run (spawning directly in Cherrygrove) is correct.
    Screenshot `shots\BUG001_silver_side_by_side.png`.
  * Mass reproduction: `scripts\scan_conn.py` crosses every one of the 144 connections (112 crossed with my sampling) and
    runs the bag open/close: **22 connections** end with at least one object whose cached tile != the slot of its sprite
    (e.g. ROUTE_29->NEW_BARK_TOWN, ROUTE_39->ROUTE_38, ROUTE_41->ROUTE_40, ROUTE_42->MAHOGANY_TOWN, ROUTE_44->MAHOGANY_TOWN,
    PEWTER->ROUTE_2, ROUTE_2->VIRIDIAN, ROUTE_21->PALLET, ROUTE_16->ROUTE_17, ROUTE_12->LAVENDER, ROUTE_11->VERMILION,
    ROUTE_4->CERULEAN, OLIVINE->ROUTE_40, ROUTE_30->ROUTE_31, ROUTE_36->ROUTE_37, AZALEA->ROUTE_33, ECRUTEAK->ROUTE_37,
    LAKE_OF_RAGE->ROUTE_43, ROUTE_46->ROUTE_45, FUCHSIA->ROUTE_19, ROUTE_13->ROUTE_14, VERMILION->ROUTE_6). The same scan on the
    base ROM (`C:\Users\xelu3\build\base0`, vanilla Spanish pokecrystal, run with `BETA_ROOT=...\alt_base0`) gives **1** (FUCHSIA<->ROUTE_19).
    Raw logs: `logs\conn_*.jsonl` (hack) and `alt_base0\logs\conn_*.jsonl` (base).
* **Root cause:** `OBJECT_SPRITE_TILE` of every object struct is cached when the struct is created (`GetSpriteVTile`, `home/map_objects.asm`).
  Since v5.0 `AddOutdoorSprites` (`engine/overworld/overworld.asm:120`) first adds the *current map's own objects*
  (`AddIndoorSprites`) and only then the group list, so the VRAM arrangement of `wUsedSprites` now depends on the map, not only on the
  map group (in the base ROM every map of a group shares the same arrangement). `MapSetupScript_Connection`
  (`data/maps/setup_scripts.asm`) does **not** rebuild the list (no `RefreshSprites`, no `LoadMapGraphics`), so objects of the new map are created
  with tiles taken from the *previous map's* arrangement. The next call to `RefreshSprites`
  (`ReloadTilesetAndPalettes`: closing PACK/POKéMON/#DEX/status/Pokégear, `ReturnToMapWithSpeechTextbox`, `reloadmap` after every battle, Fly arrival
  inside the map ...) re-sorts the list for the new map but never updates the cached `OBJECT_SPRITE_TILE` of the objects that already exist,
  so they now point at the tiles of whatever NPC occupies that slot in the new arrangement.
* **Proposed fix (any of):**
  1. (smallest, engine) at the end of `RefreshSprites` (or inside `LoadAndSortSprites`) walk the 12 object structs and re-resolve
     `OBJECT_SPRITE_TILE` with `GetSpriteVTile` (`hMapObjectIndex = OBJECT_MAP_OBJECT_INDEX`) — fixes the stale-after-refresh half;
  2. add a `mapsetup`-command to `MapSetupScript_Connection` that runs `farcall RefreshSprites` after `LoadMapAttributes` and **before**
     `LoadMapObjects` (see BUG-002: this is also what makes the arrival correct);
  3. or undo the v5.0 reordering of `AddOutdoorSprites` (go back to group-list-only) and fix the "walking NPC without walking frames" problem in the data
     by ordering each group list so that the walking sprites of that group come first (the 10 walking-capable slots).
* **Evidence:** `shots\BUG001_side_by_side.png`, `shots\BUG001_silver_side_by_side.png`, `logs\conn_*.jsonl`, `scripts\scan_conn.py`.

---

## BUG-002 — Route 29 tutorial dude (and other walkers) are drawn with background tiles while they walk; NPCs with no graphics slot are drawn as the player

* **Severity:** visual (distortion) — also affects the first minutes of the game
* **Status:** CONFIRMED (Route 29 dude: 2 scripts; arrival scan: 20 connections)
* **Reported symptom:** "Route 29 tutorial dude's sprite distorts while he walks"; "NPCs in Goldenrod drawn with another NPC's graphics".
* **Reproduction:** `py -3.12 -W ignore scripts\repro_bug002.py` (and the visual strip `scripts\repro_bug002b.py`
  -> `shots\BUG002_walk_control_vs_bug.png`).
  1. New game state, spawn `NEW_BARK_TOWN` (2, 9) (`wNewBarkTownSceneID`=1 so the Teacher does not stop you), walk left into Route 29.
  2. At x=53 the catch-tutorial coord event starts: the dude (SPRITE_COOLTRAINER_M) walks to you.
  * Expected: normal walking animation (control: spawning directly in Route 29 is fine). Actual: while he steps, his 4 OAM entries use tile ids
    156-159 of VRAM bank 0 (BG tile data) — an orange block of tileset garbage replaces him for the whole walk
    (`shots\BUG002_walk_control_vs_bug.png`, right column). `oam_check` reports 4 bad OAM entries per frame.
* **Root cause:** same as BUG-001. New Bark's arrangement (own objects first: TEACHER, FISHER, RIVAL, CHRIS, KRIS then the group list) places
  `SPRITE_COOLTRAINER_M` at tile 152, i.e. in the **second tile table** (`>= $80`, VRAM bank 0, standing frames only: `GetUsedSprite` never copies the
  walking half there and `InitSprite` clears the bank-1 bit). Route 29 objects keep that slot because the connection does not rebuild the list. A walking
  step uses facing tile ids `+$80`, i.e. `$9c..$9f` of bank 0 = background tiles.
* **Path matrix for the Ulex-warning dude** (`py -3.12 -W ignore scripts\dude_matrix.py`, OAM sampled every 2 frames from spawn to the end of the
  dialogue; "bad" = samples with non-sprite tiles in OAM): arriving from **New Bark Town on foot** = 20 bad samples, dude in tile slot 152 (any time of
  day: morning/day/night, any weekday incl. Tuesday, on foot or on the bike); spawning directly in Route 29 = 0 (dude in slot 12);
  walking in from Cherrygrove (west connection) = 0 (slot 108, the Cherrygrove list happens to keep him in table 1); arriving through the Route 46 gate
  warp = only one transient sample at the warp itself. This is why the earlier door/connection/menu scripts (which spawn inside the map or walk
  Cherrygrove->Route 29) never saw it: **the bad path is the one every new game takes (New Bark -> Route 29 -> the dude's coord event at x=53)**.
  The scene fires 100 % of the time on that path, so every player sees the dude replaced by background tiles while he walks UP/RIGHT.
* **Mass evidence:** `scripts\scan_conn_arrival.py` (log `logs\arr_*.jsonl`): after arriving by connection, objects of the new map
  * with **no slot at all** (GetSpriteVTile falls back to the player's tiles, so they are drawn as the player): 10 connections, e.g.
    ROUTE_35->GOLDENROD_CITY (11 objects: POKEFAN_M, COOLTRAINER_F x2, ROCKET x7, POKEFAN_M), GOLDENROD_CITY->ROUTE_35 (FISHER, BUG_CATCHER, SUPER_NERD),
    ROUTE_33->ROUTE_32 (FISHER x4, COOLTRAINER_M, 2 POKE_BALLs), FUCHSIA->ROUTE_19 (swimmers), ROUTE_3->ROUTE_4 (LASS x2), ROUTE_29->NEW_BARK (KRIS), ROUTE_27->NEW_BARK (CHRIS, KRIS), ...
  * **walking-type** sprites with walking movement stuck in the standing-only table: 10 connections (ROUTE_44->MAHOGANY (GRAMPS), ROUTE_1->PALLET (TEACHER),
    ROUTE_21->PALLET, ROUTE_19->FUCHSIA (TEACHER), ROUTE_4->CERULEAN (COOLTRAINER_M), ROUTE_41->CIANWOOD (POKEFAN_M), ROUTE_5/24/9->CERULEAN (COOLTRAINER_M), ROUTE_33->AZALEA (GRAMPS)).
* **Proposed fix:** rebuild the sprite list on arrival through a connection (fix 2 of BUG-001), or restore a group-wide arrangement.
  Verification script: `scan_conn_arrival.py` must report no `missing` and no `t2walk`.

---

## BUG-003 — CRASH: choosing a different move while locked by a Choice item (Banda/Gafas/Pañuelo Elegidos) resets the game

* **Severity:** crash (reset to the "Este cartucho está diseñado..." boot screen). Very likely **the reported "INVERSIÓN / REVERSAL crash"**: the
  three Choice items are in every new game's starting bag (10 each, infinite) and REVERSAL/FLAIL are exactly the moves players pick *after* having used
  something else once their Pokémon is low on HP. The move itself is innocent (see "Negative results" below).
* **Status:** CONFIRMED (deterministic with all three items; also found independently by the random battle fuzzer, 2 of 2 replays).
* **Reproduction:** `py -3.12 -W ignore scripts
epro_choice_crash.py` (about 20 s).
  New Bark ambush battle (walk left at (4,2)), Mewtwo with moves [HARDEN, PSYCHIC] holding item $2d / $32 / $5a, use HARDEN on turn 1, open the move menu
  on turn 2 and choose PSYCHIC. Output: `item 2d: CRASH (reset)`, `item 32: CRASH`, `item 5a: CRASH`, `item 00: no crash`.
  The fuzzer record that found it: `logs\chaos_0.jsonl` line `it=34` (replay `scripts
epro_chaos.py 0 34 1 2`, `repro_chaos2.py 0 34 1` prints the call chain).
* **Expected:** the text "El objeto elegido fija el ataque." and back to the move menu. **Actual:** garbage text, execution runs into an undefined opcode
  (`rst $38` reached from `TextCommand_DOTS` via `DoTextUntilTerminator`), the console resets.
* **Root cause:** `engine/battle/core.asm`, `MoveSelectionScreen`: `.choice_locked` loads `hl = .ChoiceLockedText` (a text defined inline in the battle-core bank)
  and falls into `.place_textbox_start_over: call StdBattleTextbox`. `StdBattleTextbox` (`home/battle.asm`: "print battle text at 20:hl") switches to
  `BANK(BattleText)` (bank $20) before printing, so it reads the pointer in the wrong bank (here $20:65fd, which is the code of the debug tileset editor).
  The other two messages of that routine (`BattleText_TheMoveIsDisabled`, `BattleText_TheresNoPPLeftForThisMove`) live in `data/text/battle.asm` and work.
  I checked every other `StdBattleTextbox` call site in engine/ for a label outside `data/text/battle.asm`: this is the only one.
* **Proposed fix:** move the three lines of `.ChoiceLockedText` to `data/text/battle.asm` (e.g. `BattleText_ChoiceLocked`) and load that label; or
  replace the `call StdBattleTextbox` of that single path by `call BattleTextbox` (which uses the current bank).
* **Evidence:** `logs\chaos_*.jsonl`, `scripts
epro_choice_crash.py`, `scripts
epro_chaos2.py` (stack: `MoveSelectionScreen.place_textbox_start_over -> StdBattleTextbox -> BattleTextbox -> PrintTextboxText -> PlaceString -> DoTextUntilTerminator -> TextCommand_DOTS -> rst $38`).

### Negative results for the REVERSAL report (so nobody searches in the wrong place)
* All 254 moves used by the player (`scripts\moves_battle.py player`, Mewtwo with the single move, New Bark ambush) and by the enemy
  (`... enemy`, the 4 enemy move slots overwritten at the first steady menu): 0 resets, FLAIL (175) and REVERSAL (179) included, with several HP/MaxHP combinations
  (`work/reversal2.py` scenarios too). The Flail/Reversal power code (`BattleCommand_ConstantDamage`) is byte-identical to the base ROM apart from address shifts.
* Summary screen, move info screen and battle subpanel with INVERSIÓN in slot 1-4: no problem (`scripts	_summary.py`).

---
