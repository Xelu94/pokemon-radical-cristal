"""Worker: talk to every object_event of one map (new-game event state, strong party), record the dialogue.
argv: MAPSTEM [only_object_index ...]      env: PLAYER_GENDER, TOD (0 morn,1 day,2 nite; default untouched)
Prints 'RESULT {json}' with per-object results.
"""
import sys, json, traceback
sys.path.insert(0, 'scripts')
from lib import *
import objs
alarm(560)
stem = sys.argv[1]
only = {int(a) for a in sys.argv[2:]}
const = objs.const_of(stem)
pm = objs.parse_map(stem)
res = {'map': stem, 'const': const, 'objects': []}


def box_present(rows):
    return len(rows) >= 6 and rows[0].startswith('+') and rows[5].startswith('+')


def talk(o, spawn, face):
    sx, sy = spawn
    g = G(const, sx, sy)
    try:
        if os.environ.get('WEAK') == '1':
            g.party([19, 16, 10], level=5)
            for i_ in range(3):
                at_ = g.a('wPartyMonNicknames') + 11 * i_
                g.p.memory[at_:at_ + 11] = [0x8c, 0x84, 0x96, 0x93, 0x96, 0x8e, 0x50, 0, 0, 0, 0]
            g.write('wJohtoBadges', 0xff)
            g.p.memory[g.a('wPlayerName'):g.a('wPlayerName') + 5] = [0x93, 0x88, 0x93, 0x8e, 0x50]
        else:
            strong_party(g, level=100)
        g.p.tick(40)
        start = g.pos()
        if start != (sx, sy):
            return {'spawn_fail': True}
        if os.environ.get('FREEZE', '1') == '1':
            for b in range(13):
                a = g.a('wObjectStructs') + b * 40
                if g.p.memory[a + 1] == o['idx'] and g.p.memory[a] != 0:
                    g.p.memory[a + 3] = 1          # SPRITEMOVEDATA_STILL: stop wandering / walking
            g.p.tick(24)
        g.press(face, 12, hold=6)
        g.press('a', 20, hold=4)
        frames, seen = [], set()
        idle = 0
        last_txt = None
        flags = set()
        npress = 0
        battle = False
        for step in range(130):
            g.p.tick(10)
            if crashed(g):
                flags.add('CRASH'); break
            if g.read('wBattleMode') != 0:
                battle = True
                for _bi in range(80):
                    g.press('a', 24, hold=6)
                    if _bi < 12:
                        rows_b = decode_rows(g, range(13, 17))
                        tb_ = ' / '.join(r_[1:-1].strip() for r_ in rows_b if r_[1:-1].strip())
                        if tb_ and 'quiere' in tb_ and tb_ not in seen:
                            seen.add(tb_); frames.append('[BATTLE] ' + tb_)
                            if os.environ.get('SHOTBATTLE') == '1':
                                Path('shots/tr').mkdir(parents=True, exist_ok=True)
                                g.p.screen.image.convert('RGB').save('shots/tr/%s_%d.png' % (stem, o['idx']))
                    if g.read('wBattleMode') == 0 and settled(g):
                        break
                    if crashed(g):
                        flags.add('CRASH_IN_BATTLE'); break
                if 'CRASH_IN_BATTLE' in flags:
                    break
                g.p.tick(60)
                continue
            if not settled(g):
                continue
            rows = decode_rows(g, range(12, 18))
            if box_present(rows):
                idle = 0
                txt = ' / '.join(r[1:-1].strip() for r in rows[1:5] if r[1:-1].strip())
                if txt != last_txt:
                    last_txt = txt
                    continue                      # still printing: wait for a stable frame
                if txt not in seen:
                    seen.add(txt)
                    frames.append(txt)
                    if '{' in txt:
                        flags.add('GARBAGE')
                g.press('a', 10, hold=4)
                last_txt = None
                npress += 1
                if npress > 100:
                    flags.add('HANG_TEXT'); break
            else:
                full = [r for r in decode_rows(g) if r]
                if full and curmap(g) == const and any(('|' in r or '+' in r) for r in full):
                    key = ' | '.join(full)
                    if key not in seen:
                        seen.add(key)
                        frames.append('[UI] ' + key[:200])
                idle += 1
                if idle > 8:
                    break
                if idle > 3:
                    g.press('b', 10, hold=4)
        r = {'party_after': g.party_species() if settled(g) else None, 'frames': frames, 'flags': sorted(flags), 'battle': battle, 'map_after': curmap(g), 'pos': g.pos()}
        if not frames and not battle and curmap(g) == const and g.pos() == start:
            r['no_response'] = True
        if crashed(g):
            r['crash'] = True
            r['shot'] = shot(g, 'npc_crash_%s_%d' % (stem, o['idx']))
        return r
    finally:
        g.close()


for o in pm['objects']:
    if only and o['idx'] not in only:
        continue
    item = {'idx': o['idx'], 'x': o['x'], 'y': o['y'], 'sprite': o['sprite'], 'script': o['script'], 'type': o['type'],
            'move': o['move'], 'flag': o['flag']}
    try:
        OVERRIDES['clear'] = [o['flag']] if o['flag'] not in ('-1', '0') else []
        OVERRIDES['set'] = [x for x in os.environ.get('SETFLAGS', '').split(',') if x]
        order = [((o['x'], o['y'] + 1), 'up'), ((o['x'] - 1, o['y']), 'right'), ((o['x'] + 1, o['y']), 'left'),
                 ((o['x'], o['y'] - 1), 'down')]
        tries = []
        for spawn, face in order:
            if spawn[0] < 0 or spawn[1] < 0:
                continue
            r = talk(o, spawn, face)
            tries.append((spawn, face, r.get('no_response', False), r.get('spawn_fail', False)))
            if r.get('spawn_fail'):
                continue
            if not r.get('no_response'):
                item.pop('no_response', None); item.update(r); item['spawn'] = spawn
                break
            item.update(r)
        item['tries'] = len(tries)
        if item.get('no_response'):
            item['spawn'] = None
    except Exception as e:
        item['error'] = repr(e)[:200] + traceback.format_exc()[-300:]
    res['objects'].append(item)
print('RESULT ' + json.dumps(res, ensure_ascii=True))
