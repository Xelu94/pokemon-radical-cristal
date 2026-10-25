"""Monkey test: random button mashing in a rich state (full bag, six varied Pokemon incl. egg and Dark Lugia, PC filled) in several places.
argv: scene seed [inputs=4000]     scenes: pokecenter | route | mart | gym | goldenrod
Detects: crash screen ('cartucho'), program counter running in RAM/VRAM, exception.   env PLAYER_GENDER
"""
import sys, json, random, traceback
sys.path.insert(0, 'scripts')
from lib import *
alarm(560)
scene = sys.argv[1]; seed = int(sys.argv[2]); n_in = int(sys.argv[3]) if len(sys.argv) > 3 else 4000
rnd = random.Random(seed)
spots = {
    'pokecenter': ('GOLDENROD_POKECENTER_1F', 6, 6),
    'route': ('ROUTE_29', 30, 14),
    'mart': ('GOLDENROD_DEPT_STORE_1F', 7, 8),
    'gym': ('VIOLET_GYM', 4, 14),
    'goldenrod': ('GOLDENROD_CITY', 14, 20),
    'blackthorn': ('BLACKTHORN_POKECENTER_1F', 6, 6),
}
const, x, y = spots[scene]
out = {'scene': scene, 'seed': seed, 'gender': os.environ.get('PLAYER_GENDER', '0')}
try:
    g = G(const, x, y)
    # six varied mons (ids): Mewtwo, Dark Lugia(252), Smeargle(235), Chansey(113), Pikachu, Egg(253)
    species = [150, 252, 235, 113, 25, 253]
    g.party(species, level=70)
    for i in range(6):
        base = g.a('wPartyMon1') + (g.a('wPartyMon2') - g.a('wPartyMon1')) * i
        mv = rnd.sample(range(1, 252), 4)
        g.p.memory[g.a('wPartyMon1Moves') + (g.a('wPartyMon2') - g.a('wPartyMon1')) * i:g.a('wPartyMon1Moves') + (g.a('wPartyMon2') - g.a('wPartyMon1')) * i + 4] = mv
        g.p.memory[g.a('wPartyMon1PP') + (g.a('wPartyMon2') - g.a('wPartyMon1')) * i:g.a('wPartyMon1PP') + (g.a('wPartyMon2') - g.a('wPartyMon1')) * i + 4] = [20] * 4
        g.p.memory[g.a('wPartyMon1ID') + (g.a('wPartyMon2') - g.a('wPartyMon1')) * i:g.a('wPartyMon1ID') + (g.a('wPartyMon2') - g.a('wPartyMon1')) * i + 2] = g.p.memory[g.a('wPlayerID'):g.a('wPlayerID') + 2]
        for stat in ['MaxHP', 'HP', 'Attack', 'Defense', 'Speed', 'SpclAtk', 'SpclDef']:
            g.p.memory[g.a('wPartyMon1' + stat) + (g.a('wPartyMon2') - g.a('wPartyMon1')) * i:g.a('wPartyMon1' + stat) + (g.a('wPartyMon2') - g.a('wPartyMon1')) * i + 2] = [1, 200]
    for i in range(6):
        at = g.a('wPartyMonNicknames') + 11 * i
        g.p.memory[at:at + 11] = [0x8c, 0x84, 0x96, 0x93, 0x96, 0x8e, 0x50, 0, 0, 0, 0]
    g.write('wJohtoBadges', 0xff); g.write('wKantoBadges', 0xff)
    g.p.memory[g.a('wStatusFlags')] |= 1
    g.p.memory[g.a('wPokedexCaught'):g.a('wPokedexCaught') + 32] = [0xff] * 32
    g.p.memory[g.a('wPokedexSeen'):g.a('wPokedexSeen') + 32] = [0xff] * 32
    g.p.memory[g.a('wPokegearFlags')] = 0x1f
    g.p.memory[g.a('wPlayerName'):g.a('wPlayerName') + 5] = [0x93, 0x88, 0x93, 0x8e, 0x50]
    # bag: legal contents only (ITEM pocket ids in wItems, balls in wBalls, key items in wKeyItems, TMs in wTMsHMs)
    att = open('work/source/data/items/attributes.asm', encoding='utf8').read()
    pockets = re.findall(r'^\s*item_attribute [^,]+,[^,]+,[^,]+,[^,]+,\s*(\w+),', att, re.M)
    byp = {}
    for idx, pk in enumerate(pockets, 1):
        if idx >= 255: continue
        byp.setdefault(pk, []).append(idx)
    def fill(numsym, listsym, ids, qty, cap):
        pick = rnd.sample(ids, min(cap, len(ids)))
        g.write(numsym, len(pick))
        raw = []
        for i_ in pick:
            raw += [i_, qty]
        raw.append(255)
        g.p.memory[g.a(listsym):g.a(listsym) + len(raw)] = raw
    fill('wNumItems', 'wItems', byp['ITEM'], 5, 50)
    fill('wNumBalls', 'wBalls', byp['BALL'], 9, 12)
    fill('wNumKeyItems', 'wKeyItems', byp['KEY_ITEM'], 1, 22)
    for i_ in range(57):
        g.p.memory[g.a('wTMsHMs') + i_] = rnd.choice([0, 1, 3])
    g.write('wMoney', 0);
    g.p.memory[g.a('wMoney'):g.a('wMoney') + 3] = [0x0f, 0x42, 0x3f]
    g.p.tick(60)
    buttons = ['a'] * 6 + ['b'] * 3 + ['up'] * 3 + ['down'] * 3 + ['left'] * 2 + ['right'] * 2 + ['start', 'select']
    maps_seen = set()
    ring = []
    ring_imgs = []
    sp = 0
    for k in range(n_in):
        b = rnd.choice(buttons)
        g.p.button_press(b)
        g.p.tick(rnd.choice([2, 4, 8]))
        g.p.button_release(b)
        g.p.tick(rnd.choice([4, 10, 20]))
        if os.environ.get('SHOTS_FROM') and k >= int(os.environ['SHOTS_FROM']):
            ring_imgs.append((k, b, frame(g)))
        if os.environ.get('LOG') == '1':
            ring.append((k, b, ' | '.join(r_ for r_ in decode_rows(g) if r_)[:160]))
            ring = ring[-70:]
        if k % 25 == 0:
            if crashed(g):
                out['ring'] = ring[-45:]
                if ring_imgs:
                    cols = 8; imgs = [im for _, _, im in ring_imgs][-32:]
                    sh_ = Image.new('RGB', (160 * cols, 144 * ((len(imgs) + cols - 1) // cols)))
                    for j_, im in enumerate(imgs):
                        sh_.paste(im, ((j_ % cols) * 160, (j_ // cols) * 144))
                    sh_.save('shots/monkey_seq_%s_%d_g%s.png' % (scene, seed, out['gender']))
                    out['seq'] = [(k_, b_) for k_, b_, _ in ring_imgs][-32:]
                out['crash'] = {'input': k, 'shot': shot(g, 'monkey_crash_%s_%d_g%s' % (scene, seed, out['gender']))}
                break
            pc = g.p.register_file.PC
            if 0x8000 <= pc < 0xff80:
                sp += 1
                if sp >= 3:
                    out['pc_in_ram'] = {'input': k, 'pc': hex(pc)}
                    out['shot'] = shot(g, 'monkey_pc_%s_%d_g%s' % (scene, seed, out['gender']))
                    break
            else:
                sp = 0
            if settled(g):
                maps_seen.add(curmap(g))
    out['maps'] = sorted(maps_seen)
    g.close()
except Exception as e:
    out['error'] = repr(e)[:200] + traceback.format_exc()[-300:]
print('RESULT ' + json.dumps(out, ensure_ascii=True))
