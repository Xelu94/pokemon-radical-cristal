"""Shared helpers for the GOLD beta-test scripts.
Run every script with the current directory = C:\\Users\\xelu3\\build\\beta\\gold (so work/... resolves).

    py -3.12 -W ignore scripts/<name>.py [args] | grep -v INFO

Provides:
  G                 : Game + StoryMixin (PyBoy 2.8.1 harness; player is GOLD unless PLAYER_GENDER=1)
  sprite_info()     : id -> (name, type, tiles)  (names are exact, unlike work/slots.py which is shifted by one)
  structs(g)        : the 13 object structs decoded
  mapobjs(g)        : the 15 map objects decoded
  check_objects(g)  : static sprite consistency oracle (see below)
  oam_check(g)      : per-frame distortion oracle (every visible OAM tile must be real sprite/emote data)
  safe(g)           : True if WRAM reads are trustworthy
"""
import faulthandler
import os
import re
import sys
import io
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf8")
except Exception:
    pass
HERE = Path(os.environ.get('BETA_ROOT') or Path(__file__).resolve().parent.parent)
os.chdir(HERE)
base = Path('work/test-v43-changes.py').read_text(encoding='utf8')
exec(base[:base.index('# --- Starting inventory')])      # defines Game, maps, items, root, check
sys.path.insert(0, 'work')
from story_helper import StoryMixin, EVENTS            # noqa: E402
from PIL import Image                                   # noqa: E402

SRC = HERE / 'work' / 'source'

_PyBoy_orig = PyBoy
RAM_FILE = [None]          # set to a BytesIO before creating a G to give the emulator (and capture) its SRAM


def PyBoy(rom, **kw):      # shadows pyboy.PyBoy inside Game.__init__ (same module namespace)
    if RAM_FILE[0] is not None:
        kw['ram_file'] = RAM_FILE[0]
        import struct, time
        kw['rtc_file'] = io.BytesIO(struct.pack('d', time.time()) + bytes(9) + bytes(8) + struct.pack('d', time.time()))
    return _PyBoy_orig(rom, **kw)



def _engine_flags():
    """ENGINE_* name -> (wram symbol, bit)."""
    consts = {}
    for line in (SRC / 'constants/ram_constants.asm').read_text(encoding='utf8').splitlines():
        m = re.match(r'\s*const (\w+_F)\s*; (\d+)', line)
        if m:
            consts[m[1]] = int(m[2])
    names = []
    for line in (SRC / 'constants/engine_flags.asm').read_text(encoding='utf8').splitlines():
        m = re.match(r'\s*const (ENGINE_\w+)', line)
        if m:
            names.append(m[1])
    entries = []
    for line in (SRC / 'data/events/engine_flags.asm').read_text(encoding='utf8').splitlines():
        m = re.match(r'\s*engine_flag (\w+), (\w+)', line)
        if m:
            bit = consts.get(m[2])
            if bit is None and m[2].isdigit():
                bit = int(m[2])
            entries.append((m[1], bit))
    return {n: e for n, e in zip(names, entries)}


ENGINE = _engine_flags()


def _init_script_lines():
    text = (SRC / 'engine/events/std_scripts.asm').read_text(encoding='utf8')
    body = text[text.index('InitializeEventsScript:'):]
    body = body[:body.index('endcallback')]
    return [l.strip() for l in body.splitlines()[1:] if l.strip()]


def new_game_init(g):
    """Replay InitializeEventsScript (what PlayersHouse2F's callback runs in a real new game). The stock harness
    skips it, which leaves ~100 'hidden' NPCs visible and every wVariableSprites entry at 0."""
    for line in _init_script_lines():
        m = re.match(r'(setevent|clearevent) (\w+)', line)
        if m:
            g.set_event(m[2], m[1] == 'setevent')
            continue
        m = re.match(r'setflag (\w+)', line)
        if m:
            sym, bit = ENGINE[m[1]]
            addr = g.a(sym) + bit // 8
            g.p.memory[addr] = g.p.memory[addr] | (1 << (bit % 8))
            continue
        m = re.match(r'variablesprite (\w+), (\w+)', line)
        if m:
            g.p.memory[g.a('wVariableSprites') + SPRITE_NAMES_REV[m[1]] - 0xf0] = SPRITE_NAMES_REV[m[2]]
            continue
        if line.startswith('checkevent') or line.startswith('iftrue') or line.startswith('.skip') or line.startswith('end'):
            continue
    g.set_event('EVENT_INITIALIZED_EVENTS')


def set_clock(g, hour=None, weekday=None):
    """Force the in-game clock: hour 0..23 (MORN 4-9, DAY 10-17, NITE 18-3), weekday 0=Sun..6=Sat (VAR_WEEKDAY)."""
    rtc_h = g.p.memory[g.a('hRTCHours')] if 'hRTCHours' in g.symbols else 0
    if hour is not None:
        g.write('wStartHour', (hour - rtc_h) % 24)
    if weekday is not None:
        rtc_d = g.p.memory[g.a('hRTCDayLo')]
        g.write('wStartDay', (weekday - rtc_d) % 7)
    g.p.tick(10)


class G(StoryMixin, Game):
    """Game + StoryMixin that (by default) runs InitializeEventsScript's effects just before the first map loads, like
    a real New Game. Pass init=False (or env NEWGAME=0) for the stock, uninitialised harness state."""

    def __init__(self, mapname, x, y, init=None, hour=None, weekday=None, rom=None, clear=(), setev=(), wram=(), gender=None):
        if init is None:
            init = os.environ.get('NEWGAME', '1') != '0'
        self._init = init
        self._hour, self._weekday = hour, weekday
        self._clear, self._setev, self._wram = list(clear), list(setev), list(wram)
        self._hooked = False
        Game.__init__(self, mapname, x, y)

    # Game.__init__ is reused; we intercept its PyBoy construction through a property hook on 'p'.
    @property
    def p(self):
        return self.__dict__['_p']

    @p.setter
    def p(self, value):
        self.__dict__['_p'] = value
        if not self._hooked and (self._init or self._clear or self._setev or self._wram or self._hour is not None or self._weekday is not None):
            self._hooked = True
            bank, addr = self.symbols['OverworldLoop']
            value.hook_register(bank, addr, self._on_overworld_loop, None)

    def _on_overworld_loop(self, _):
        if not self.__dict__.get('_did_init'):
            self.__dict__['_did_init'] = True
            if self._init:
                new_game_init(self)
            for e in self._clear:
                self.set_event(e, False)
            for e in self._setev:
                self.set_event(e, True)
            for n, v in self._wram:
                self.write(n, v)
            if self._hour is not None or self._weekday is not None:
                set_clock(self, self._hour, self._weekday)

    def reload_map(self):
        """Close/open the start menu: runs ReloadTilesetAndPalettes/RefreshSprites like returning from any menu."""
        self.press('start', 30)
        self.press('b', 30)
        self.p.tick(30)


def arm(seconds):
    faulthandler.dump_traceback_later(seconds, exit=True)


# ---------------------------------------------------------------- constants
def _sprite_names():
    names = {}
    n = -1
    for line in (SRC / 'constants/sprite_constants.asm').read_text(encoding='utf8').splitlines():
        m = re.match(r'\s*const (SPRITE_\w+)', line)
        if m:
            n += 1
            names[n] = m[1]
        if re.match(r'\s*const_next \$80', line):
            n = 0x7f
        if re.match(r'\s*const_next \$e0', line):
            n = 0xdf
        if re.match(r'\s*const_next \$f0', line):
            n = 0xef
        if 'SPRITE_NONE' in line and 'const ' in line:
            n = 0
            names[0] = 'SPRITE_NONE'
    return names


SPRITE_NAMES = _sprite_names()
SPRITE_NAMES_REV = {v: k for k, v in SPRITE_NAMES.items()}
TYPES = {1: 'WALKING', 2: 'STANDING', 3: 'STILL'}


def sprite_name(i):
    return SPRITE_NAMES.get(i, hex(i))


def map_name_by_ids(group, number):
    for k, v in maps.items():
        if v == [group, number]:
            return k
    return '?%d,%d' % (group, number)


def rom_sprite(g, sid):
    """(rom_offset_of_gfx, tiles, type) of overworld sprite id sid (1..NUM_OVERWORLD_SPRITES)."""
    bank, addr = g.symbols['OverworldSprites']
    off = bank * 0x4000 + addr - 0x4000 + (sid - 1) * 6
    r = g.rom
    a = r[off] | r[off + 1] << 8
    size = r[off + 2]
    b = r[off + 3]
    typ = r[off + 4]
    return b * 0x4000 + a - 0x4000, size >> 4, typ


def variable(g, sid):
    """Resolve sprite ids >= 0xf0 through wVariableSprites. Returns real id (0 -> WALKING fallback = 1)."""
    if sid >= 0xf0:
        v = g.p.memory[g.a('wVariableSprites') + sid - 0xf0]
        return v if v else 1
    return sid


def is_mon_sprite(sid):
    return 0x80 <= sid < 0xf0


def safe(g):
    return g.read('wBattleMode') == 0 and (g.p.memory[0xff70] & 7) in (0, 1)


# ---------------------------------------------------------------- decoders
OBJ_LEN = 40


def structs(g):
    a = g.a('wObjectStructs')
    out = []
    for i in range(13):
        b = list(g.p.memory[a + i * OBJ_LEN:a + i * OBJ_LEN + OBJ_LEN])
        out.append(dict(i=i, sprite=b[0], mapidx=b[1], tile=b[2], move=b[3], flags1=b[4], flags2=b[5],
                        pal=b[6], walking=b[7], direction=b[8], step_type=b[9], action=b[0xb], facing=b[0xd],
                        x=b[0x10], y=b[0x11], raw=b))
    return out


def mapobjs(g):
    a = g.a('wMap1Object')
    out = []
    for k in range(15):
        b = list(g.p.memory[a + k * 16:a + k * 16 + 16])
        out.append(dict(idx=k + 1, structid=b[0], sprite=b[1], y=b[2], x=b[3], move=b[4], radius=b[5],
                        hour1=b[6], hour2=b[7], pal_type=b[8], sight=b[9],
                        script=b[10] | b[11] << 8, flag=b[12] | b[13] << 8))
    return out


def used(g):
    u = list(g.p.memory[g.a('wUsedSprites'):g.a('wUsedSprites') + 64])
    out = []
    for i in range(0, 64, 2):
        if not u[i]:
            break
        out.append((u[i], u[i + 1]))
    return out


# ---------------------------------------------------------------- oracles
def check_objects(g, verbose=False):
    """Static oracle. Returns list of (code, detail) problems:
       NOT_IN_LIST   object sprite has no VRAM slot (it would be drawn with the player's tiles)
       STALE_TILE    the tile cached in the object struct differs from the slot of its sprite
       MAPOBJ_DIFF   object struct sprite differs from its map object sprite
       VRAM_BAD      the VRAM tiles of a slot differ from the ROM graphics for that sprite
       T2_WALKER     a WALKING-type sprite that is placed in the second tile table (>=0x80: no walking frames)
                     AND whose object is not standing/still (it would be drawn with BG tiles while it walks)
    """
    problems = []
    lst = used(g)
    slot = {}
    for sid, t in lst:
        slot.setdefault(sid, t)
    mo = mapobjs(g)
    for s in structs(g):
        if s['i'] == 0 or s['sprite'] == 0:
            continue
        sid = s['sprite']
        if sid not in slot:
            problems.append(('NOT_IN_LIST', 'struct %d sprite %s mapidx %d' % (s['i'], sprite_name(sid), s['mapidx'])))
            continue
        exp = slot[sid]
        if s['tile'] != exp and not is_mon_sprite(sid):
            problems.append(('STALE_TILE', 'struct %d %s tile %d != slot %d (mapidx %d)' % (s['i'], sprite_name(sid), s['tile'], exp, s['mapidx'])))
        if 1 <= s['mapidx'] <= 15:
            if mo[s['mapidx'] - 1]['sprite'] != sid:
                problems.append(('MAPOBJ_DIFF', 'struct %d %s but map object %d says %s' % (s['i'], sprite_name(sid), s['mapidx'], sprite_name(mo[s['mapidx'] - 1]['sprite']))))
    # slot content
    for sid, t in lst:
        real = variable(g, sid)
        if is_mon_sprite(real) or real == 0 or real > 0x67:
            continue
        off, n, typ = rom_sprite(g, real)
        if n == 0:
            continue
        vbk = 1 if t < 0x80 else 0
        base_addr = 0x8000 + (t & 0x7f) * 16
        got = bytes(g.p.memory[vbk, base_addr:base_addr + n * 16])
        want = bytes(g.rom[off:off + n * 16])
        if got != want:
            problems.append(('VRAM_BAD', 'slot %s tile %d first half' % (sprite_name(sid), t)))
        elif t < 0x80 and typ != 3:
            got2 = bytes(g.p.memory[1, base_addr + 0x800:base_addr + 0x800 + n * 16])
            if got2 != bytes(g.rom[off + n * 16:off + 2 * n * 16]):
                problems.append(('VRAM_BAD', 'slot %s tile %d walking half' % (sprite_name(sid), t)))
    return problems


def table2_walkers(g):
    """WALKING sprites living in table 2 whose objects are present (these can never show walking frames)."""
    out = []
    lst = used(g)
    slot = {}
    for sid, t in lst:
        slot.setdefault(sid, t)
    for s in structs(g):
        if s['i'] == 0 or s['sprite'] == 0:
            continue
        sid = s['sprite']
        real = variable(g, sid)
        if is_mon_sprite(real) or real > 0x67 or sid not in slot:
            continue
        off, n, typ = rom_sprite(g, real)
        if typ == 1 and slot[sid] >= 0x80:
            out.append((s['i'], sprite_name(sid), s['mapidx'], s['move']))
    return out


def mapobj_slots(g):
    """For every map object of the current map: (idx, sprite name, movement, slot tile or None, real type or None)."""
    lst = used(g)
    slot = {}
    for sid, t in lst:
        slot.setdefault(sid, t)
    out = []
    for o in mapobjs(g):
        sid = o['sprite']
        if sid == 0:
            continue
        real = variable(g, sid)
        typ = None
        if not is_mon_sprite(real) and 1 <= real <= 0x67:
            typ = rom_sprite(g, real)[2]
        out.append(dict(idx=o['idx'], sprite=sprite_name(sid), real=sprite_name(real), move=o['move'], x=o['x'], y=o['y'],
                        slot=slot.get(sid), type=TYPES.get(typ), flag=o['flag']))
    return out


_valid_cache = {}


def valid_tile_set(g):
    """Set of 16-byte tile blobs that may legally appear in an OAM entry right now: all tiles of all sprite sheets in
    wUsedSprites (both halves), player sheet, emotes, shadow/grass, plus blank."""
    key = (tuple(used(g)), bytes(g.p.memory[g.a('wVariableSprites'):g.a('wVariableSprites') + 16]))
    if key in _valid_cache:
        return _valid_cache[key]
    s = {bytes(16)}
    for sid, t in used(g):
        real = variable(g, sid)
        if is_mon_sprite(real) or real == 0 or real > 0x67:
            continue
        off, n, typ = rom_sprite(g, real)
        for k in range(n * (1 if typ == 3 else 2)):
            s.add(bytes(g.rom[off + k * 16:off + k * 16 + 16]))
    _valid_cache.clear()
    _valid_cache[key] = s
    return s


def oam_entries(g):
    raw = list(g.p.memory[0xfe00:0xfea0])
    out = []
    for i in range(40):
        y, x, tile, attr = raw[i * 4:i * 4 + 4]
        if y == 0 or y >= 160 or x == 0 or x >= 168:
            continue
        out.append((i, y, x, tile, attr))
    return out


def oam_check(g, extra_valid=None):
    """Returns list of OAM entries whose tile data is not a legal overworld sprite tile (distortion)."""
    valid = valid_tile_set(g)
    bad = []
    mon_tiles = set()
    for sid, t in used(g):
        if is_mon_sprite(variable(g, sid)):
            for k in range(12):
                mon_tiles.add((1 if t < 0x80 else 0, (t & 0x7f) + k))
                mon_tiles.add((1 if t < 0x80 else 0, (t & 0x7f) + k + 0x80))
    for i, y, x, tile, attr in oam_entries(g):
        bank = (attr >> 3) & 1
        if (bank, tile) in mon_tiles:
            continue
        if bank == 1 and tile >= 0xf8:
            continue            # emote / shadow / grass area (see data/sprites/emotes.asm)
        data = bytes(g.p.memory[bank, 0x8000 + tile * 16:0x8000 + tile * 16 + 16])
        if data not in valid:
            bad.append((i, y, x, tile, attr, bank))
    return bad


def shot(g, name, scale=3):
    im = g.p.screen.image.convert('RGB')
    im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
    os.makedirs('shots', exist_ok=True)
    im.save('shots/%s.png' % name)
    return 'shots/%s.png' % name


def strong_party(g, species=150, level=100, moves=(94,)):
    g.party([species], level=level)
    for stat in ['MaxHP', 'HP', 'Attack', 'Defense', 'Speed', 'SpclAtk', 'SpclDef']:
        g.p.memory[g.a('wPartyMon1' + stat):g.a('wPartyMon1' + stat) + 2] = [3, 231]
    for k, m in enumerate(moves):
        g.p.memory[g.a('wPartyMon1Moves') + k] = m
        g.p.memory[g.a('wPartyMon1PP') + k] = 30
    pid = g.a('wPlayerID')
    g.p.memory[g.a('wPartyMon1ID'):g.a('wPartyMon1ID') + 2] = [g.p.memory[pid], g.p.memory[pid + 1]]   # obey (OT id == player id)
    g.write('wJohtoBadges', 0xff)
    g.write('wKantoBadges', 0xff)
    g.p.memory[g.a('wPlayerName'):g.a('wPlayerName') + 5] = [0x93, 0x88, 0x93, 0x8e, 0x50]
    at = g.a('wPartyMonNicknames')
    g.p.memory[at:at + 11] = [0x8c, 0x84, 0x96, 0x93, 0x96, 0x8e, 0x50, 0, 0, 0, 0]


def where(g):
    return map_name_by_ids(*g.mem('wMapGroup', 2)), g.pos()


def settle(g, n=90):
    g.p.tick(n)


def crashed(g):
    return 'cartucho' in ' '.join(g.screen_text())


def pack_cycle(g):
    """Open the start menu, enter MOCHILA (2nd entry when the party exists), close it: CloseSubmenu -> ReloadTilesetAndPalettes
    -> RefreshSprites (sprite list rebuilt for the current map while object structs keep their cached tiles)."""
    g.press('start', 30)
    g.press('down', 12)
    g.press('a', 50)
    g.press('b', 50)
    g.press('b', 50)
    g.p.tick(40)
    settle_ok(g)


def settle_ok(g, tries=40):
    """Wait until the overworld is steady: safe WRAM reads, valid map group, no text box."""
    for _ in range(tries):
        if safe(g) and 1 <= g.read('wMapGroup') <= 26 and g.read('wMapNumber') >= 1:
            return True
        g.p.tick(15)
    return False


def party_cycle(g):
    g.press('start', 30)
    g.press('a', 50)
    g.press('b', 50)
    g.press('b', 50)
    g.p.tick(40)


def objs_in_view(g):
    return [(s['i'], sprite_name(s['sprite']), s['tile'], s['mapidx'], s['x'], s['y']) for s in structs(g) if s['sprite'] and s['i']]


# ---------------------------------------------------------------- source parsing (objects, signs, warps)
def stem_to_const():
    names = re.findall(r'^\s*map (\w+),', (SRC / 'data/maps/maps.asm').read_text(encoding='utf8'), re.M)
    consts = re.findall(r'^\s*map_const (\w+)', (SRC / 'constants/map_constants.asm').read_text(encoding='utf8'), re.M)
    return dict(zip(names, consts))


TOD = {'MORN': 1, 'DAY': 2, 'NITE': 4}


def parse_map(stem):
    text = (SRC / 'maps' / (stem + '.asm')).read_text(encoding='utf8')
    objs = []
    for m in re.finditer(r'^\s*object_event\s+(-?\d+),\s*(-?\d+),\s*(\w+),\s*(\w+),\s*(-?\d+),\s*(-?\d+),\s*(-?\d+),\s*(-?\w+),\s*(\w+),\s*(\w+),\s*(-?\d+),\s*(\w+),\s*(-?\w+)', text, re.M):
        objs.append(dict(kind='obj', x=int(m[1]), y=int(m[2]), sprite=m[3], move=m[4], hour=int(m[7]), tod=TOD.get(m[8], None) if not re.match(r'-?\d+$', m[8]) else int(m[8]), pal=m[9],
                         type=m[10], sight=int(m[11]), script=m[12], flag=m[13]))
    bgs = []
    for m in re.finditer(r'^\s*bg_event\s+(-?\d+),\s*(-?\d+),\s*(\w+),\s*(\w+)', text, re.M):
        bgs.append(dict(kind='bg', x=int(m[1]), y=int(m[2]), type=m[3], script=m[4]))
    warps = [(int(m[1]), int(m[2]), m[3], int(m[4])) for m in re.finditer(r'^\s*warp_event\s+(-?\d+),\s*(-?\d+),\s*(\w+),\s*(-?\d+)', text, re.M)]
    return objs, bgs, warps


def text_box(g):
    """Rows 12-17 of the screen text (the dialogue box), stripped."""
    rows = g.screen_text()
    return [r for r in rows[12:18]]


def tilemap_rows(g):
    raw = g.mem('wTilemap', 360)
    return [raw[r * 20:(r + 1) * 20] for r in range(18)]


def script_running(g):
    return g.read('wScriptRunning') != 0


def _charmap():
    cm = {}
    for line in (SRC / 'constants/charmap.asm').read_text(encoding='utf8').splitlines():
        m = re.match(r'\s*charmap "(.)",\s*\$([0-9a-fA-F]{2})', line)
        if m:
            cm.setdefault(int(m[2], 16), m[1])
    cm[0x7f] = ' '
    return cm


CHARMAP = _charmap()


def screen_text2(g, rows=range(18), unknown='□'):
    """Tilemap decoded with the real charmap (accents, punctuation). Unknown tile ids -> unknown char."""
    raw = g.mem('wTilemap', 360)
    out = []
    for r in rows:
        out.append(''.join(CHARMAP.get(t, unknown) for t in raw[r * 20:(r + 1) * 20]).rstrip())
    return out


# ---------------------------------------------------------------- battles
def in_battle(g):
    """True when a battle is running and WRAM reads are trustworthy (svbk 1)."""
    return (g.p.memory[0xff70] & 7) == 1 and g.read('wBattleMode') != 0


def battle_menu(g):
    t = ' '.join(screen_text2(g))
    return 'LUCHA' in t and ('HUIR' in t or 'MOCHILA' in t)


def fight(g, max_iter=900, moves=4, log=None, slow=False):
    """Drive a battle to its end with a strong party. Returns ('end'|'crash'|'timeout', iterations).
    Cycles through the 4 moves when the enemy HP does not drop (immunities)."""
    slot = 0
    last_hp, stuck = None, 0
    started = False
    for it in range(max_iter):
        t = ' '.join(g.screen_text())
        if 'cartucho' in t:
            return 'crash', it
        svbk = g.p.memory[0xff70] & 7
        if svbk == 1 and g.read('wBattleMode') != 0:
            started = True
        if started and svbk in (0, 1) and g.read('wBattleMode') == 0:
            return 'end', it
        if svbk == 1 and g.read('wBattleMode') != 0 and battle_menu(g):
            hp = g.p.memory[g.a('wEnemyMonHP')] * 256 + g.p.memory[g.a('wEnemyMonHP') + 1]
            if hp == last_hp:
                stuck += 1
                if stuck >= 2:
                    slot = (slot + 1) % moves
                    stuck = 0
            else:
                stuck = 0
            last_hp = hp
            g.press('up', 4, hold=4); g.press('left', 4, hold=4)
            g.press('a', 20, hold=6)          # LUCHA
            for _ in range(3):
                g.press('up', 4, hold=4)
            for _ in range(slot):
                g.press('down', 4, hold=4)
            g.press('a', 20, hold=6)
            if log is not None:
                log.append((it, 'move', slot, hp))
            continue
        g.press('a', 14, hold=6)
    return 'timeout', max_iter


def strong_party_multi(g, level=100, moves=(94, 85, 89, 247)):
    strong_party(g, level=level, moves=moves)


def select_move(g, n):
    """In the battle move menu: put the cursor on move n (1-based) using wMenuCursorY, then do not press A."""
    for _ in range(6):
        cur = g.read('wMenuCursorY')
        if cur == n:
            return True
        g.press('down', 5, hold=4)
    return g.read('wMenuCursorY') == n
