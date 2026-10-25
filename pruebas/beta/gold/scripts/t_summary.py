from lib import *
g = G('NEW_BARK_TOWN', 6, 8, hour=12)
strong_party(g, moves=(179, 175, 94, 33))
g.p.tick(60)
g.press('start', 30)
print(screen_text2(g)[:14])
g.press('a', 40)   # POKEMON
print(screen_text2(g)[:16])
g.press('a', 40)   # first mon -> submenu
print(screen_text2(g))
g.press('a', 40)   # first item (STATS)
print('STATS page1'); print('\n'.join(screen_text2(g)))
for pg in range(3):
    g.press('right', 40)
    print('--- right', pg+1); print('\n'.join(screen_text2(g)))
g.press('a', 40)
print('--- A on moves'); print('\n'.join(screen_text2(g)))
g.press('a', 40)
print('--- A again'); print('\n'.join(screen_text2(g)))
shot(g, 'summary_moves')
g.close()
