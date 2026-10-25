"""REPRO: Cherrygrove rival scene entered from Route 29 on foot (list built for Route 29) vs after the fight (reloadmap).
usage: py -3.12 -W ignore scripts/t_repro_silver.py [route29|route30|warp]   (PLAYER_GENDER env)
Reports Silver's (SPRITE_RIVAL) tile slot / audit before the fight and after it.
route29: spawn ROUTE_29 west edge and walk east into Cherrygrove.  route30: spawn ROUTE_30 south edge and walk south.
warp: spawn directly in CHERRYGROVE_CITY (control)."""
import sys; sys.path.insert(0, 'scripts')
from lib import *
alarm(400)
mode = sys.argv[1] if len(sys.argv) > 1 else 'route29'
OVERRIDES['write'] = [('wCherrygroveCitySceneID', 1)]
if mode == 'route29':
    g = G('ROUTE_29', 0, 6); key = 'left'          # Route 29 west side connects to Cherrygrove (east edge there)
elif mode == 'route30':
    g = G('ROUTE_30', 6, 53); key = 'down'
else:
    g = G('CHERRYGROVE_CITY', 39, 6); key = None
strong_party(g, level=50)
g.set_event('EVENT_GOT_TOTODILE_FROM_ELM')
g.write('wCherrygroveCitySceneID', 1)
g.p.tick(60)
print('start', curmap(g), g.pos(), 'list', len(used_sprites(g)))
if key:
    for _ in range(4):
        g.press(key, 16, hold=18)
    g.p.tick(60)
    print('after crossing', curmap(g), g.pos())
slot = {s: t for s, t in used_sprites(g)}
print('RIVAL(4) slot in list before the scene:', slot.get(4), '| player slot', slot.get(g.read('wPlayerSprite')))
print('listing', listing(g)[:13])
if curmap(g) == 'CHERRYGROVE_CITY':
    # walk along the road to the scene trigger (33,6 / 33,7) by pressing left; the rival appears and talks
    imgs = []
    g.p.button_press('left')
    seen_rival = False
    for i in range(700):
        g.p.tick(3)
        s = [b for b in structs(g) if b[0] == 4 and b[1] == 2]
        if s and not seen_rival:
            seen_rival = True
            print('rival struct tile at appear:', s[0][2], 'list says', slot.get(4), 'frame', i, 'audit', audit(g))
            imgs.append(frame(g))
        if g.pos()[0] <= 34 and i % 40 == 0:
            g.p.button_release('left')
        if i % 60 == 0:
            imgs.append(frame(g))
        if g.read('wBattleMode') != 0:
            break
    g.p.button_release('left')
    print('battle started?', g.read('wBattleMode'))
    after_imgs = []
    for i in range(300):
        g.press('a', 24, hold=6)
        sv = [b for b in structs(g) if b[0] == 4 and b[1] == 2]
        if sv and g.read('wBattleMode') == 0 and settled(g):
            sl = {s_: t_ for s_, t_ in used_sprites(g)}
            if len(after_imgs) < 14 and sv[0][2] != sl.get(4):
                base = sv[0][2]
                ents = [(y_, x_) for (i_, y_, x_, t_, a_) in oam_list(g) if ((a_ >> 3) & 1) == 1 and (base <= t_ < base + 12 or base + 128 <= t_ < base + 140)]
                if ents:
                    x0 = max(0, min(160 - 40, min(e[1] for e in ents) - 12)); y0 = max(0, min(144 - 40, min(e[0] for e in ents) - 22))
                    after_imgs.append(('f', frame(g).crop((x0, y0, x0 + 40, y0 + 40)).resize((160, 160), Image.NEAREST)))
            if sv[0][2] != sl.get(4) and not any(a_[0] == 'silver' for a_ in after_imgs):
                print('AFTER FIGHT: Silver struct tile', sv[0][2], 'but list slot for SPRITE_RIVAL is', sl.get(4), '-> drawn with', [n_ for n_ in listing(g) if n_.strip().startswith(str(sv[0][2]))])
                after_imgs.append(('silver', frame(g)))
                imgs.append(frame(g))
        if g.read('wBattleMode') == 0 and settled(g) and g.event('EVENT_RIVAL_CHERRYGROVE_CITY') and i > 10:
            break
    g.p.tick(60)
    print('after fight:', curmap(g), g.pos(), 'audit', audit(g))
    fr_ = [im for k_, im in after_imgs if k_ == 'f'][:12]
    if fr_:
        sh_ = Image.new('RGB', (160 * len(fr_), 160), (255, 255, 255))
        for k_, im in enumerate(fr_): sh_.paste(im, (160 * k_, 0))
        sh_.save('shots/silver_after_fight_%s_g%s.png' % (mode, os.environ.get('PLAYER_GENDER', '0')))
        print('saved shots/silver_after_fight_%s_g%s.png' % (mode, os.environ.get('PLAYER_GENDER', '0')))
g.close()
