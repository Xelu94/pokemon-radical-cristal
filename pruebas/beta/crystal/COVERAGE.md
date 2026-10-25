# Coverage - beta test of Radical Cristal v5.3, girl player (CRISTAL, `PLAYER_GENDER=1`); boy run where noted

Folder `C:\Users\xelu3\build\beta\crystal`; commands are run from it. Everything uses `scripts\lib.py` (class `G`), which adds to the stock harness:
the real new-game event state (`InitializeEventsScript`: hidden NPCs + `wVariableSprites`, see BUGS.md header), forced time of day / weekday (`HOUR`, `DAYNUM`),
`WILD=1` (encounter on every cave step), `FIXCONN=1` (proposed fix patch for BUG-001), `BASEROOT` (compare with another ROM tree).
Parallelism never exceeded 3 Python processes (`scripts\prun.py` runs workers as subprocesses with a per-job timeout; a hung emulator is reported as HANG).

## Re-verification on the lead's fixed build
Connection scan girl + boy: 0 problems (127 crossings); dude walk, Silver after the fight, charscan, NPC sweep (1512 objects), fuzz (379 maps), 251 moves x2, monkey (75 runs),
story test (28 PASS), eggs: all clean. See the STATUS table in BUGS.md. The tables below describe the first (pre-fix) run unless stated.

## Done

| Area | What was run | Result |
|---|---|---|
| Sprite list / VRAM, every map at spawn | `t_audit_all.py` (384 maps, boy & girl state), `fullcheck`/`audit`/`oam_orphans` (VRAM vs ROM graphics for every object, struct tile vs list, OAM ownership) | clean at spawn (ECRUTEAK_POKECENTER_1F spawn is held by Bill's scene) |
| Doors / warps | `w_trans.py` over 387 maps: every warp approached from both sides, out / back / out again, checks after each arrival (about 980 successful passages, girl) | 0 sprite problems. `FastShip1F` warp 0 (`LAST_MAP`, -1) resets when spawned without a previous map: harness artifact, same in vanilla |
| Map connections | `w_conn.py` over all 68 maps with connections: 127 of 142 crossings performed (15 blocked by harness/cut trees); girl, boy, base0 ROM, and with the fix patch | **BUG-001/002/003/004** (20 crossings affected; 0 with the fix) |
| Reported sprite issues | Silver after the Cherrygrove fight, the Route 29 dude (frame-by-frame OAM walk), Route 29 teacher/old man stale tiles, paths: warp, New Bark connection, Cherrygrove connection, Route 46 gate, Start menu, bike, surf state, wild battle, Save + soft reset + Continue | all reproduced / explained, see BUGS.md (`t_dude_paths.py`, `t_dude_distort.py`, `t_repro_silver.py`, `t_savecontinue.py`) |
| Random walking fuzz | `w_fuzz.py` seeds 1-3, every map, 60-120 steps, battles auto-mashed, sprite Watch on | with `FIXCONN=1` only two false positives (map-name banner OAM, Hall of Fame sparkle) |
| NPC dialogue | `w_npc.py`: every `object_event` of 354 maps (1512 objects) spoken to at night, 07:00 and 14:00 (girl), plus 7 weekdays on the 19 maps with weekday logic | 0 crashes, 0 garbage glyphs, 0 text hangs; remaining no-response objects are flag/scene-gated (Bill scene in Ecruteak PC, Goldenrod roof sale, decorations, Sudowoodo, Rocket base security) |
| Trainers | 386 trainer objects fought with a level-100 Mewtwo (win path); class names cross-checked with the source (`t_trainer_names.py`: 306/310 equal, 4 differences are other trainers' line of sight); battle intro sheets `shots\trainers_page1..6.png` (pages 1, 4, 5 reviewed) | no crash/hang; pictures consistent with class |
| All 254 moves | `w_move.py` (player uses / enemy uses, wild, 3 turns each); `w_tmove.py` trainer battle with all AI layers, enemy moves 1-254 in groups of 4; REVERSAL/FLAIL with 17 current/max HP pairs for both sides and AI on | 0 crashes. **The reported REVERSAL (INVERSION, 179) crash did not reproduce in any variant** |
| Menu monkey | `w_monkey.py` 144 runs x 5000 random button presses (boy+girl, Pokecenter / route / mart / gym / Blackthorn / Goldenrod, random legal bag, 6 varied Pokemon incl. egg and Dark Lugia, Pokedex and Pokegear unlocked) | 0 crashes / runaway PC (an earlier 5 crashes came from an invalid bag in my harness and were discarded: `logs\invalid`) |
| Rare Candy selector | `w_candy.py`: all 251 species from level 5, +40 levels at once, random move offers, evolutions | no crash; **BUG-006** (HM moves offered and unforgettable) |
| Evolution stones | `w_stone.py`: every `EVOLVE_ITEM` entry (20) | all evolve correctly. No trade/happiness evolutions remain (static check `t_evocheck.py`) |
| Nuzlocke capture rule | `t_nuz_capture.py`: first encounter of the zone caught with a Master Ball, second refused with the NUZLOCKE text | as documented |
| Other protagonist (girl = GOLD) | `w_ambush.py`: New Bark, Sprout Tower 3F, Indigo Plateau final fight, Gold's home; text, battle pictures (Gold front picture, Kris back picture), potion, egg, heal; boy run for the same | all work; battle intro "GOLD RIVAL quiere luchar." (name then class, same order as every trainer). Dragon's Den ambush needs Tuesday/Thursday + rival event: set up in the script but not driven to the end |
| Elm | `t_elm_full.py`: duel with a full party: the three shiny starters go to the PC ("fue enviado al PC de BILL") | ok |
| Super League | lead's `work\test-v45-story.py` rerun as girl: 28 PASS; rooms' dialogues through `w_npc.py` (win and loss texts both seen) | ok |
| Eggs | `w_egg.py`: 8 hatches, all shiny, all first-stage non-legendary | ok |
| Dark Lugia | `t_darklugia.py` (summary screen, Pokedex, battle) | front picture and type text ok |
| Static lints | `t_textlint.py` (28,323 strings, width 18), `t_charscan.py` (unmapped characters), `t_spritehash.py` (sprite table), marts listing, `t_outdoor_lists.py` | **BUG-005**; `CableClubGroupSprites` has only 11 entries instead of 23 (only indoor maps use that group, harmless today) |
| Level caps | read of `GetCurrentLevelCap` vs docs | matches (Johto 19-53, 65 until Hall of Fame, Kanto 67-85, 95, 100) |

## Not done / limits

* **Real hardware / other emulators.** PyBoy does not model VRAM access timing. The reported REVERSAL crash (and the earlier Ice Beam note) are said to come
  from a mobile emulator; they cannot be judged here. The proposed BUG-001 fix rebuilds about 300 tiles with the screen on during a connection scroll: check on real
  hardware / BGB for flicker before shipping.
* Full story playthrough from the intro (the harness skips Oak's speech): I jumped between maps with the new-game state and set scene variables; the order-dependent
  chains (Mt Mortar, Rocket takeover, Red, etc.) were not replayed event by event.
* Not driven to the end: the Dragon's Den ambush (needs Tue/Thu and the Mt Moon rival flag; setup in `w_ambush.py dragon`, no final capture), Ulex loss path across all 16 locations
  (`t_ulex_loss.py` runs one; only the win path was run for all 16), Tito's trade and move reminder menus (only entered through `w_npc.py`), Joy nurses (talked to, heal not verified),
  Pokegear phone/radio, mobile / link / trade rooms, Battle Tower, PC withdraw/deposit with all boxes full, bag full gifts, shop buy/sell sequences, Day-Care, Safari-less Bug Contest.
* Connections that the harness could not cross: Violet-Route 31 (east), Azalea-Route 34, Ecruteak-Route 38 / 42 west edges, Route 29-46, Route 36-35, Route 17/16/18,
  Route 15, Route 12, Route 6, Route 5, Saffron-Route 8 (listed as NOCROSS in `logs\conn_*.jsonl`).
* Boy runs: connections, monkey, ambush and story texts only; the NPC sweep and the fuzz were run as girl.
* Sandbox ROM (`pokecristal_debug.gbc`) was not exercised.
