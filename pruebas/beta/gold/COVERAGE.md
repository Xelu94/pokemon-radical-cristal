# COVERAGE.md — GOLD (boy) beta run

All numbers are from the scripts in `scripts\` (logs in `logs\`). State = real new-game state (`InitializeEventsScript` replayed by `scripts/lib.py`,
class `G`), player GOLD (no `PLAYER_GENDER`), 12:00 unless stated.

## What was covered

| Area | How | Result |
|---|---|---|
| Sprite lists of all 394 maps | `scan_maps.py`, 3 times of day (06/12/20 h), + start-menu refresh | no object without slot, no stale tile, no walker in the standing-only table at spawn (static state is clean); Ecruteak Pokémon Center / Tin Tower 1F flagged only while their arrival scenes run (known false positives) |
| Map connections (144 directed; 112 crossed on foot with my sampling) | `scan_conn.py` (+ Pack open/close), `scan_conn_arrival.py`, `repro_conn.py`, `repro_arrival.py` | **BUG-001 / BUG-002**; base ROM (`alt_base0`) comparison: 1/112 vs 22/112 |
| Route 29 "Ulex warning" dude, whole walk, OAM sampled every 2 frames | `dude_matrix.py` (12 arrival paths/times/weekdays/bike), `repro_bug002*.py` | bad only when arriving from New Bark (**BUG-002**) |
| Cherrygrove / Silver first battle | `repro_silver.py` | **BUG-001** visible (Silver and Guide Gent drawn with other NPCs) |
| Buildings/caves/stairs warps, both directions, with menu refresh | `transitions2.py` (790 warps; ~640 completed both ways, ~150 could not be walked automatically: stairs/ladders inside dungeons) | no sprite problem (stale/missing/VRAM/walker) |
| Save in-game and CONTINUE | `t_save.py` (New Bark) | sprite list rebuilt correctly after Continue (no bug) — only 1 map tried |
| Time of day / weekday | `G(hour=, weekday=)`, `t_hour.py`, scans at 3 hours, dude matrix (Tuesday) | clock control works; no time-dependent sprite problem found |
| Talk to every object_event / bg_event (1512 + 792) | `talk_sweep.py` (new-game state, hidden flags cleared per object, approach from 4 sides) | 2255+ interactions: 0 crashes, 0 garbage tiles inside dialogue boxes, charset clean; 104 "no_script" (hidden items need the Itemfinder/other facing, objects hidden by time/flags); ~64 "hang" are interactive menus (marts, Tito menu, Academy blackboard, puzzles, PC) that need B |
| Every trainer / leader battle found by the sweep (334) | `trainer_sweep.py` (Mewtwo Lv100 4 moves) | 334/334 battles end, 0 crash; post-battle script idle in all but 2 menu cases; money rewards present (Electrode "trainers" give none by design); no sprite problem after battles |
| All 254 moves used by the player and by the enemy | `moves_battle.py player|enemy` (Mewtwo / ambush Rattata) | 0 crash (FLAIL 175, REVERSAL 179 included) |
| Random battle fuzz (species, level, HP/MaxHP, 4 random moves, held items incl. Choice items, enemy moves/items/HP) | `chaos_battle.py`: 240 + 1000 + 1200 (the last 1200 without player Choice items) battles | 5 crashes, **all** BUG-003 (player holding a Choice item); 0 crashes in the 1200 without Choice items |
| Random-button fuzz in the overworld/menus with a full bag/party/Pokégear/dex (about 250 000 presses) | `menu_fuzz.py` 122 runs x 1500-2500 presses, 6 maps, 3 times of day | 0 crashes (an earlier crash was my own invalid party: species $ff) |
| Marts (static) | parse of `data/items/marts.asm` | no healing items; evolution stones in Cianwood, Goldenrod 2F, Olivine, Ecruteak, Mahogany, Blackthorn and every Kanto town mart; counts match |
| Items from the bag in the overworld | `items_use.py` : 56 usable Items-pocket entries + Key Items | 0 crash |
| Elm duel, other protagonist (4 ambushes, home/Zurullo trade), Super League (lobby, Azul win/loss, Ulex/Tito loss texts, champion reward), Silver Cave guard, refused battle, Sudowoodo variable sprite, Gold berries, ball->Max Potion, prices | lead's `test-v45-story.py` re-run with the initialised state (`story_regress.py`, log `logs/story_regress3.log`) | 26 PASS, 2 FAIL: both are the Elm check being read before the three gift-naming screens finish; played to the end (`t_elm.py`) the duel gives Feraligatr+Meganium+Typhlosion (shiny), flags clear, HP intact |

## What I could not cover (and why)

* Girl player (`PLAYER_GENDER=1`) — the task is the GOLD run.
* Full walkthrough with real walking through the story (intro, Mom, Elm's lab, each gym by walking) — replaced by spawn-based sweeps with initialised events; story gates set via flags in specific scripts only (Silver, Route 29 dude, Elm duel).
* Dex sort modes, PC box full/Bill's PC, Pokégear tabs/phone, Joy nurses (only "talk" status), mart buy/sell flows, evolutions (levels/stones/happiness/trade), breeding and 10-step shiny eggs, Rare Candy quantity selector 1-99, TMs, level caps/whiteout/Nuzlocke death marking — not exercised in this run (time spent on the sprite and crash reports). The Rare Candy and Nuzlocke code were only read.
* Fly / Teleport arrival: inspected (they use the Warp map-setup script, which rebuilds the list) but not run through the real menu.
* Surf: player sprite state tested only through bike (`wPlayerState`), not by really surfing.
* Sandbox ROM (`pokecristal_debug.gbc`) menus and its 41 travel destinations.
* Hidden items (BGEVENT_ITEM) need the exact facing tile: reported `no_script`.
* Ulex roaming encounters (16 locations) and Tito fights were only reached through the generic talk/trainer sweeps (state "new": most Ulex scripts need a badge, status `done`).
* The elevator / link / trade / colosseum / Copycat 2F / Battle Tower maps (emulator hangs, per the brief).

## Script index (run from `C:\Users\xelu3\build\beta\gold`: `py -3.12 -W ignore scripts\<name>.py <args> | grep -v INFO`)

* `lib.py` — shared harness (`G` with new-game init, clock control, oracles `check_objects`/`mapobj_slots`/`oam_check`, `fight`, `pack_cycle`, parsers). Env `BETA_ROOT` points to another tree (e.g. `alt_base0` for the vanilla ROM), `NEWGAME=0` = stock uninitialised state.
* Sprites: `scan_maps.py`, `scan_conn.py`, `scan_conn_arrival.py`, `transitions2.py`, `dude_matrix.py`, `repro_bug001.py`, `repro_bug002.py`, `repro_bug002b.py`, `repro_silver.py`, `repro_conn.py`, `repro_arrival.py`, `t_save.py`.
* Crash: `repro_choice_crash.py` (BUG-003), `chaos_battle.py`, `repro_chaos.py`, `repro_chaos2.py`, `moves_battle.py`, `menu_fuzz.py`.
* Sweeps: `talk_sweep.py` (add `- battle` as 5th arg for battle candidates), `trainer_sweep.py`, `summarize_trainers.py`, `items_use.py`, `story_regress.py`.
* Parallel jobs were launched as `scan_conn.py w 3`, `talk_sweep.py w 3 new`, etc. (w = 0..2, at most 3 processes). Raw output: `logs\*.jsonl`; screenshots: `shots\`.
