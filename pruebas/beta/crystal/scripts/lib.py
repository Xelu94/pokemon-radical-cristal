"""Shared helpers for the beta-tester scripts. Run from the beta folder (cwd = C:/Users/xelu3/build/beta/crystal).
Usage in a script:   import sys; sys.path.insert(0,'scripts'); from lib import *
"""
import sys, os, re, io, faulthandler
from pathlib import Path
sys.path.insert(0, 'work')
_base = Path('work/test-v43-changes.py').read_text(encoding='utf8')
_src = _base[:_base.index('# --- Starting inventory')]
# hook point: after set_emulation_speed(0) the game calls self._hook() (used to inject the 'new game' event state)
_src = _src.replace("self.p.set_emulation_speed(0)\n", "self.p.set_emulation_speed(0)\n        self._hook()\n", 1)
_src = _src.replace("    def texts(self, labels):", "    def _hook(self):\n        pass\n\n    def texts(self, labels):", 1)
_src = _src.replace("        spawn = self.offset('SpawnPoints')", "        self._patch(data)\n        spawn = self.offset('SpawnPoints')", 1)
_src = _src.replace("    def texts(self, labels):", "    def _patch(self, data):\n        pass\n\n    def texts(self, labels):", 1)
exec(_src)      # Game, maps, items, root
from story_helper import StoryMixin, EVENTS
from PIL import Image


EVENTS['EVENT_ULEX_LOCATION_BASE'] = EVENTS['EVENT_V3_SHRINE_ENCOUNTER'] + 1
EVENTS['EVENT_ULEX_BADGE_BASE'] = EVENTS['EVENT_ULEX_LOCATION_BASE'] + 16
EVENTS['EVENT_TITO_TRADE_BASE'] = 400


def flagnum(expr):
    m = re.match(r'(\w+)\s*\+\s*(\d+)$', expr.strip())
    if m:
        return EVENTS[m[1]] + int(m[2])
    return EVENTS[expr.strip()]


def set_flag_number(g, n, value=True):
    addr = g.a('wEventFlags') + n // 8
    bit = n % 8
    b = g.p.memory[addr]
    g.p.memory[addr] = (b | (1 << bit)) if value else (b & ~(1 << bit) & 0xff)


OVERRIDES = {'set': [], 'clear': [], 'write': []}   # applied after the new-game state, before the map loads


def _initscript_lines():
    t = (root / 'engine/events/std_scripts.asm').read_text(encoding='utf8')
    body = t[t.index('InitializeEventsScript:'):]
    body = body[:body.index('endcallback')]
    return [l.strip() for l in body.splitlines()]


class G(StoryMixin, Game):
    """Game with the real 'new game' state: the intro skips PlayersHouse2F whose callback runs InitializeEventsScript
    (hides hundreds of NPCs by flag and sets wVariableSprites). Set env NEWSTATE=0 for the bare harness state."""
    def _patch(self, data):
        if os.environ.get('WILD') == '1':       # every grass step is an encounter
            o = self.offset('TryWildEncounter.EncounterRate')
            data[o:o + 2] = bytes([0x37, 0xc9])
        if os.environ.get('FIXCONN') == '1':    # proposed fix test: connection crossing rebuilds the sprite list
            cmds = re.findall(r'^\s*add_mapsetup (\w+)', (root / 'data/maps/setup_script_pointers.asm').read_text(encoding='utf8'), re.M)
            o = self.offset('MapSetupScript_Connection')
            t, gfx = cmds.index('LoadMapTileset'), cmds.index('LoadMapGraphics')
            end = o
            while data[end] != 0xff:
                end += 1
            body = data[o:end]
            i = body.index(bytes([t]))
            data[o + i] = gfx

    def _hook(self):
        if os.environ.get('HOUR') is not None:
            self.fake_hour = int(os.environ['HOUR'])
            self.fake_day = int(os.environ['DAYNUM']) if os.environ.get('DAYNUM') else None
            self.p.hook_register(*self.symbols['GetTimeOfDay'], lambda _: self._fake_time(), None)
        if os.environ.get('NEWSTATE', '1') == '0':
            self.p.hook_register(*self.symbols['_InitializeStartDay'], lambda _: self.apply_overrides(), None)
            return
        self.p.hook_register(*self.symbols['_InitializeStartDay'], lambda _: (self.newgame_state(), self.apply_overrides()), None)

    def _fake_time(self):
        self.p.memory[self.a('hHours')] = self.fake_hour
        if self.fake_day is not None:
            self.p.memory[self.a('wCurDay')] = self.fake_day

    def apply_overrides(self):
        for n in OVERRIDES['clear']:
            set_flag_number(self, flagnum(n), False)
        for n in OVERRIDES['set']:
            set_flag_number(self, flagnum(n), True)
        for (n, v) in OVERRIDES['write']:
            self.p.memory[self.a(n)] = v

    def newgame_state(self):
        for l in _initscript_lines():
            m = re.match(r'setevent (\w+)', l)
            if m:
                self.set_event(m[1]); continue
            m = re.match(r'variablesprite (\w+), (\w+)', l)
            if m:
                self.p.memory[self.a('wVariableSprites') + SPR_ID[m[1]] - 0xf0] = SPR_ID[m[2]]; continue
            if l == 'setflag ENGINE_ROCKET_SIGNAL_ON_CH20':
                self.p.memory[self.a('wStatusFlags')] |= 1 << 4
            if l == 'setflag ENGINE_ROCKETS_IN_MAHOGANY':
                self.p.memory[self.a('wStatusFlags2')] |= 1 << 7


def alarm(n=580):
    faulthandler.dump_traceback_later(n, exit=True)


# ---- sprite tables --------------------------------------------------------------------------------------------
SPR = {}
for _l in (root / 'constants/sprite_constants.asm').read_text(encoding='utf8').splitlines():
    _m = re.match(r'\s*const (SPRITE_\w+)\s*;\s*([0-9a-f]{2})\s*$', _l)
    if _m:
        SPR[int(_m[2], 16)] = _m[1]
SPR[0x67] = 'SPRITE_TITO_XELUIS'
SPR_ID = {v: k for k, v in SPR.items()}
STYPE = {}
STYPE_NAME = {1: 'WALK', 2: 'STAND', 3: 'STILL'}
_i = 0
for _l in (root / 'data/sprites/sprites.asm').read_text(encoding='utf8').splitlines():
    _m = re.match(r'\s*overworld_sprite (\w+), (\d+), (\w+),', _l)
    if _m:
        _i += 1
        STYPE[_i] = {'WALKING_SPRITE': 1, 'STANDING_SPRITE': 2, 'STILL_SPRITE': 3}[_m[3]]


def sname(i):
    return SPR.get(i, hex(i))


# ---- map constants ---------------------------------------------------------------------------------------------
MAPNAMES = {}   # (group, number) -> const
def _mapnames():
    group = number = 0
    for line in (root / 'constants/map_constants.asm').read_text(encoding='utf8').splitlines():
        if re.match(r'\s*newgroup ', line):
            group += 1; number = 0
        m = re.match(r'\s*map_const (\w+)', line)
        if m:
            number += 1; MAPNAMES[(group, number)] = m[1]
_mapnames()


def curmap(g):
    gr, nu = g.mem('wMapGroup', 2)
    return MAPNAMES.get((gr, nu), '?%d,%d' % (gr, nu))


def catalog():
    text = (root / 'engine/debug/sandbox_any_map_data.asm').read_text(encoding='utf8')
    out = []
    for gi, body in re.findall(r'\.Group(\d+)\n(.*?)(?=\n\.Group|\Z)', text, re.S):
        gi = int(gi)
        for m in re.finditer(r'^\s*db (\d+), (\d+), (\d+), PLAYER_\w+\s*; (\w+)', body, re.M):
            out.append((gi, int(m[1]), int(m[2]), int(m[3]), m[4]))
    return out


# ---- live state inspection -----------------------------------------------------------------------------------
def settled(g):
    return g.read('wBattleMode') == 0 and (g.p.memory[0xff70] & 7) in (0, 1)


def used_sprites(g):
    u = list(g.p.memory[g.a('wUsedSprites'):g.a('wUsedSprites') + 64])
    out = []
    for i in range(0, 64, 2):
        if not u[i]:
            break
        out.append((u[i], u[i + 1]))
    return out


def vars_(g):
    return list(g.p.memory[g.a('wVariableSprites'):g.a('wVariableSprites') + 16])


def realsprite(g, sid):
    if sid >= 0xf0:
        return vars_(g)[sid - 0xf0]
    return sid


def structs(g):
    a = g.a('wObjectStructs')
    return [list(g.p.memory[a + i * 40:a + i * 40 + 40]) for i in range(13)]


def mapobjs(g):
    a = g.a('wMap1Object')
    return [list(g.p.memory[a + k * 16:a + k * 16 + 16]) for k in range(15)]   # map object index k+1


MOVE_WALKS = {2, 3, 4, 5, 10, 0x0c, 0x0d, 0x13, 0x1a}   # wander, spinrandom, walk updown/leftright, indexed, following


def audit(g, label=''):
    """Return list of problems on the current map:
       - NOSLOT: object's sprite not in wUsedSprites (drawn with the player's tile)
       - TILE:  object struct tile differs from the tile the list assigns to that sprite
       - HIGHWALK: a WALKING_SPRITE-type graphic in the bank-0 second table (tile>=0x80) that is used by an object
                   with a walking movement (no walking frames -> distorted while walking)
    """
    probs = []
    us = used_sprites(g)
    slot = {}
    for sid, t in us:
        slot.setdefault(sid, t)
    for i, b in enumerate(structs(g)):
        sprite, mapidx, tile = b[0], b[1], b[2]
        if sprite == 0 or i == 0:
            continue
        exp = slot.get(sprite)
        real = realsprite(g, sprite)
        if exp is None:
            probs.append(('NOSLOT', i, sname(sprite), real and sname(real)))
            continue
        if exp != tile and not (real >= 0x80):
            probs.append(('TILE', i, sname(sprite), 'struct=%d list=%d' % (tile, exp)))
        if exp >= 0x80 and real and real < 0x80 and STYPE.get(real) == 1:
            mo = mapobjs(g)[mapidx - 1] if 1 <= mapidx <= 15 else None
            mv = mo[4] if mo else None
            if mv in MOVE_WALKS:
                probs.append(('HIGHWALK', i, sname(sprite), 'tile=%d move=%s obj#%s' % (exp, mv, mapidx)))
    return probs


def listing(g):
    out = []
    for sid, t in used_sprites(g):
        real = realsprite(g, sid)
        out.append('%3d %-28s %s %s' % (t, sname(sid) + ('->' + sname(real) if sid >= 0xf0 else ''),
                                        STYPE_NAME.get(STYPE.get(real if sid >= 0xf0 else sid, 0), '?'),
                                        '<=BANK0-standing-only' if t >= 0x80 else ''))
    return out


def shot(g, name):
    p = Path('shots') / (name + '.png')
    g.p.screen.image.convert('RGB').resize((480, 432), Image.NEAREST).save(p)
    return str(p)


def sheet(images, name, cols=6, scale=2):
    w, h = 160, 144
    rows = (len(images) + cols - 1) // cols
    s = Image.new('RGB', (w * cols, h * rows))
    for i, im in enumerate(images):
        s.paste(im, ((i % cols) * w, (i // cols) * h))
    s = s.resize((s.width * scale, s.height * scale), Image.NEAREST)
    p = Path('shots') / (name + '.png')
    s.save(p)
    return str(p)


def frame(g):
    return g.p.screen.image.convert('RGB').copy()


def crashed(g):
    return 'cartucho' in ' '.join(g.screen_text())


# ---- render-level check: does the VRAM behind every object's tile hold the graphics of its sprite? -------------------
_SPR_ENTRY = {}
def sprite_rom(g, real):
    """(addr_in_rom, ntiles, type) of overworld sprite id `real`"""
    b, a = g.symbols['OverworldSprites']
    off = b * 0x4000 + a - 0x4000
    e = off + (real - 1) * 6
    rom = g.rom
    addr = rom[e] | rom[e + 1] << 8
    size = rom[e + 2]; bank = rom[e + 3]; typ = rom[e + 4]
    return bank * 0x4000 + addr - 0x4000, size >> 4, typ


def fullcheck(g, label='', walk=True):
    """For the player and every object struct compare VRAM at the struct's tile with the ROM graphics of the object's sprite.
       returns list of (idx, sprite name, tile, what)"""
    bad = []
    rom = g.rom
    for i, b in enumerate(structs(g)):
        sprite, mapidx, tile = b[0], b[1], b[2]
        if sprite == 0:
            continue
        real = realsprite(g, sprite)
        if real == 0 or real >= 0x80:
            continue
        if real > 0x67:
            continue
        src, n, typ = sprite_rom(g, real)
        if n == 0:
            continue
        vbk = 1 if tile < 0x80 else 0
        base = 0x8000 + (tile & 0x7f) * 16
        got = bytes(g.p.memory[vbk, base:base + n * 16])
        if got != rom[src:src + n * 16]:
            bad.append((i, sname(sprite), tile, 'STAND-GFX-MISMATCH'))
            continue
        if walk and tile < 0x80 and typ == 1:
            got2 = bytes(g.p.memory[1, base + 0x800:base + 0x800 + n * 16])
            if got2 != rom[src + n * 16:src + 2 * n * 16]:
                bad.append((i, sname(sprite), tile, 'WALK-GFX-MISMATCH'))
        if walk and tile >= 0x80 and typ == 1 and i > 0:
            mo = mapobjs(g)[mapidx - 1] if 1 <= mapidx <= 15 else None
            if mo and mo[4] in MOVE_WALKS:
                bad.append((i, sname(sprite), tile, 'WALKER-IN-BANK0 move=%d' % mo[4]))
    return bad


# ---- OAM level check: every visible OAM tile must hold graphics that exist in the ROM's overworld sprite set -------------
_KNOWN = None
def known_tiles(g):
    global _KNOWN
    if _KNOWN is None:
        _KNOWN = set()
        rom = g.rom
        for real in range(1, 0x68):
            try:
                src, n, typ = sprite_rom(g, real)
            except Exception:
                continue
            for k in range(n * 2):          # include the second half (walking frames) generously
                _KNOWN.add(bytes(rom[src + k * 16:src + k * 16 + 16]))
        _KNOWN.add(bytes(16))
    return _KNOWN


def oam_list(g):
    out = []
    for i in range(40):
        y, x, t, a = g.p.memory[0xfe00 + i * 4:0xfe00 + i * 4 + 4]
        if y == 0 or y >= 160 or x == 0 or x >= 168:
            continue
        out.append((i, y, x, t, a))
    return out


def oam_unknown(g):
    """OAM entries whose tile data (in the bank the attribute selects) matches no overworld-sprite tile of the ROM."""
    kn = known_tiles(g)
    bad = []
    for (i, y, x, t, a) in oam_list(g):
        bank = (a >> 3) & 1
        data = bytes(g.p.memory[bank, 0x8000 + t * 16:0x8000 + t * 16 + 16])
        if data not in kn:
            bad.append((i, y, x, t, a))
    return bad


def oam_orphans(g):
    """OAM entries whose (bank, tile) lies inside no object's tile range, or whose VRAM data differs from the ROM data of the
       owning object's sprite. Emote tiles (>=0xf8 in bank 1 / emote area) and mon icons (sprite id >= 0x80) ignored."""
    rom = g.rom
    ranges = []   # (bank, lo, hi, real, src, ntiles, kind)
    for i, b in enumerate(structs(g)):
        sprite, tile = b[0], b[2]
        if sprite == 0 or b[1] == 0xff and i > 0:
            continue
        real = realsprite(g, sprite)
        if real >= 0x80 and real != 0:
            ranges.append((0 if tile >= 0x80 else 1, tile & 0x7f if tile >= 0x80 else tile, (tile & 0x7f if tile >= 0x80 else tile) + 12, real, None, 12, 0, i))
            ranges.append((0, tile, tile + 12, real, None, 12, 0, i))
            ranges.append((1, tile, tile + 12, real, None, 12, 0, i))
            ranges.append((0, 0x60, 0x80, real, None, 12, 0, i))   # LoadOverworldMonIcon target area
            continue
        if real == 0 or real > 0x67:
            continue
        src, n, typ = sprite_rom(g, real)
        if tile < 0x80:
            ranges.append((1, tile, tile + n, real, src, n, 0, i))
            if typ == 1:
                ranges.append((1, tile + 0x80, tile + 0x80 + n, real, src + n * 16, n, 1, i))
        else:
            lo = tile & 0x7f
            ranges.append((0, lo, lo + n, real, src, n, 0, i))
    bad = []
    for (idx, y, x, t, a) in oam_list(g):
        bank = (a >> 3) & 1
        if t >= 0xf8 and bank == 1:
            continue
        owner = None
        for r in ranges:
            if r[0] == bank and r[1] <= t < r[2]:
                owner = r; break
        if owner is None:
            # allow shadow/grass/dust/emote area handled by tile>=0xe0 convention; report others
            if t >= 0xe0:
                continue
            bad.append((idx, y, x, t, a, 'ORPHAN'))
            continue
        if owner[4] is None:
            continue
        data = bytes(g.p.memory[bank, 0x8000 + t * 16:0x8000 + t * 16 + 16])
        want = bytes(rom[owner[4] + (t - owner[1]) * 16:owner[4] + (t - owner[1]) * 16 + 16])
        if data != want:
            bad.append((idx, y, x, t, a, 'MISMATCH owner=%s obj#%d' % (sname(owner[3]), owner[7])))
    return bad


def strong_party(g, species=150, level=100, moves=(94,), hp=999):
    """Level `level` mon with huge stats (nicknamed so text prints)."""
    g.party([species], level=level)
    for stat in ['MaxHP', 'HP', 'Attack', 'Defense', 'Speed', 'SpclAtk', 'SpclDef']:
        g.p.memory[g.a('wPartyMon1' + stat):g.a('wPartyMon1' + stat) + 2] = [hp >> 8, hp & 255]
    g.p.memory[g.a('wPartyMon1ID'):g.a('wPartyMon1ID') + 2] = g.p.memory[g.a('wPlayerID'):g.a('wPlayerID') + 2]   # own OT: obeys at any level
    exp = int(1.25 * level ** 3)
    g.p.memory[g.a('wPartyMon1Exp'):g.a('wPartyMon1Exp') + 3] = [exp >> 16, (exp >> 8) & 255, exp & 255]
    for k, mv in enumerate(moves):
        g.p.memory[g.a('wPartyMon1Moves') + k] = mv
        g.p.memory[g.a('wPartyMon1PP') + k] = 30
    g.write('wJohtoBadges', 0xff); g.write('wKantoBadges', 0xff)
    g.p.memory[g.a('wPlayerName'):g.a('wPlayerName') + 5] = [0x93, 0x88, 0x93, 0x8e, 0x50]
    at = g.a('wPartyMonNicknames'); g.p.memory[at:at + 11] = [0x8c, 0x84, 0x96, 0x93, 0x96, 0x8e, 0x50, 0, 0, 0, 0]


class Watch:
    """Collects sprite problems seen while a scenario runs (only when reads are trustworthy)."""
    def __init__(self, g, label='', shots=True):
        self.g, self.label, self.issues, self.n, self.shots = g, label, [], 0, shots
        self.seen = set()
        self.last_map = None

    def _probs(self):
        g = self.g
        probs = []
        try:
            probs += ['FC %s' % (x,) for x in fullcheck(g)]
            probs += ['AU %s' % (x,) for x in audit(g) if x[2] != '0xff']
            probs += ['OAM %s' % (x,) for x in oam_orphans(g)]
        except Exception as e:
            probs.append('EXC ' + repr(e)[:60])
        return probs

    def check(self, tag=''):
        g = self.g
        if not settled(g):
            return
        if not any(e[1] == 76 and e[2] == 72 for e in oam_list(g)):
            return          # player not drawn at the screen centre: menu / fade / scripted scene
        self.n += 1
        probs = self._probs()
        if not probs:
            return
        # transitions (fades, map reloads) look broken for a few frames: require the same problem on 3 spaced reads
        for _ in range(3):
            g.p.tick(10)
            if not settled(g):
                return
            again = self._probs()
            if sorted(again) != sorted(probs):
                return
        key = (curmap(g), tuple(sorted(str(p) for p in probs)))
        if key not in self.seen:
            self.seen.add(key)
            name = 'w_%s_%s_%d' % (self.label, curmap(g), len(self.issues))
            path = shot(g, name) if self.shots else ''
            self.issues.append((tag, curmap(g), probs[:6], path))
            print('ISSUE', tag, curmap(g), probs[:4], path, flush=True)

    def run(self, frames, step=6):
        for _ in range(frames // step):
            self.g.p.tick(step)
            self.check('tick')


def press_watch(g, w, button='a', n=1, frames=24, hold=6):
    for _ in range(n):
        g.p.button_press(button)
        for _k in range(hold // 2):
            g.p.tick(2)
        g.p.button_release(button)
        for _k in range(frames // 3):
            g.p.tick(3)
            w.check(button)


# ---- full text decoding of the on-screen tilemap ----------------------------------------------------------------------
FULL = {}
for _l in (root / 'constants/charmap.asm').read_text(encoding='utf8').splitlines():
    _m = re.match(r'\s*charmap "(.+?)",\s*\$([0-9a-f]{2})', _l)
    if _m:
        ch, code = _m[1], int(_m[2], 16)
        if code < 0x80:
            continue
        if ch.startswith('<') and ch.endswith('>') and len(ch) == 3:
            ch = ch[1]
        if len(ch) == 1 or ch.startswith("'"):
            FULL.setdefault(code, ch)
for _c, _ch in {0x7f: ' ', 0x79: '+', 0x7a: '-', 0x7b: '+', 0x7c: '|', 0x7d: '+', 0x7e: '+', 0x60: '#', 0x6d: ':', 0x75: '…', 0x54: '#',
                0xe3: '-', 0xe8: '.', 0xe0: "'", 0xe1: 'P', 0xe2: 'K', 0xe4: '?', 0xe5: '!', 0xe6: '.', 0xe7: '/'}.items():
    FULL.setdefault(_c, _ch)


def decode_rows(g, rows=range(18)):
    raw = g.mem('wTilemap', 360)
    out = []
    for r in rows:
        line = ''
        for t in raw[r * 20:(r + 1) * 20]:
            line += FULL.get(t, ('{%02x}' % t) if t not in (0,) else ' ')
        out.append(line.rstrip())
    return out


def textbox_lines(g):
    """Rows 13 and 15 (the two text lines of the standard dialogue box, drawn at tilemap rows 14 and 16)."""
    r = decode_rows(g, range(12, 18))
    return [x.strip() for x in r]
