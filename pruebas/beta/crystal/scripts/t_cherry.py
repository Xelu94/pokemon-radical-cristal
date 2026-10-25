"""Cherrygrove first rival fight: watch sprites during/after the scene (and after leaving/returning)."""
import sys; sys.path.insert(0, 'scripts')
from lib import *
alarm(550)
g = G('CHERRYGROVE_CITY', 36, 6)
strong_party(g, level=50)
g.set_event('EVENT_GOT_A_POKEMON_FROM_ELM') if 'EVENT_GOT_A_POKEMON_FROM_ELM' in EVENTS else None
g.set_event('EVENT_GOT_TOTODILE_FROM_ELM')
g.write('wCherrygroveCitySceneID', 1)
g.p.tick(60)
w = Watch(g, 'cherry')
imgs = []
g.p.button_press('left'); 
for i in range(70):
    g.p.tick(4); w.check('walk')
g.p.button_release('left')
for i in range(260):
    press_watch(g, w, 'a', 1, 30)
    if i % 10 == 0: imgs.append(frame(g))
    if crashed(g): print('CRASH'); break
g.p.tick(120); w.check('end')
print('pos', g.pos(), curmap(g), 'rival hidden event', g.event('EVENT_RIVAL_CHERRYGROVE_CITY'))
print(sheet(imgs[:24], 'cherry_scene', cols=6, scale=1))
# leave to the south/west and return
for k in ['left'] * 4 + ['down'] * 3:
    g.press(k, 12, hold=16); w.check('post')
g.p.tick(60)
print('issues', len(w.issues))
g.close()
