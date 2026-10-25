"""BUG-001 on the exact reported scene: Route 29 -> Cherrygrove City on foot, Silver's first fight, then watch Silver walk away.
Screens: shots/SILVER_<k>.png (control = spawn directly in Cherrygrove, bug = arrive from Route 29)."""
from lib import *
arm(900)
def run(label, arrive):
    if arrive:
        g = G('ROUTE_29', 4, 6, hour=12)
    else:
        g = G('CHERRYGROVE_CITY', 38, 6, hour=12)
    strong_party(g)
    g.set_event('EVENT_GOT_TOTODILE_FROM_ELM')
    g.write('wCherrygroveCitySceneID', 1)
    g.p.tick(60)
    shots = []
    for i in range(30):
        g.press('left', 4, hold=16)
        if where(g)[0] == 'CHERRYGROVE_CITY' and g.pos()[0] <= 33: break
    for i in range(700):
        g.press('a', 20, hold=6)
        if g.read('wBattleMode') == 0 and (g.p.memory[0xff70] & 7) in (0, 1) and where(g)[0] == 'CHERRYGROVE_CITY':
            st = [s for s in structs(g) if s['sprite'] and s['i']]
            sil = [s for s in st if s['sprite'] == 4]   # SPRITE_RIVAL
            if i % 10 == 0 and sil: shots.append((i, g.p.screen.image.convert('RGB').copy(), check_objects(g)))
        if g.event('EVENT_RIVAL_CHERRYGROVE_CITY') and g.read('wCherrygroveCitySceneID') == 0 and i > 50: break
    print(label, where(g), 'scene', g.read('wCherrygroveCitySceneID'), 'frames', len(shots), [c for i, im, c in shots][-3:])
    # last frames after the fight with Silver present
    for i, im, c in shots[-1:]:
        im.resize((480, 432), Image.NEAREST).save('shots/SILVER_%s.png' % label)
    g.close()
run('control', False); run('bug', True)
