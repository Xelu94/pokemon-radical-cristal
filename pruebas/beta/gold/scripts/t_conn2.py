from lib import *
arm(300)
g = G('ROUTE_29', 57, 9, hour=12)
g.p.tick(60)
for i in range(9):
    g.press('right', 4, hold=16)
    if where(g)[0] == 'NEW_BARK_TOWN': break
g.p.tick(90)
print(where(g), objs_in_view(g), check_objects(g))
print([(sprite_name(i), t) for i, t in used(g)][:12])
a = g.p.screen.image.convert('RGB').copy()
pack_cycle(g)
print(where(g), objs_in_view(g), check_objects(g))
print([(sprite_name(i), t) for i, t in used(g)][:12])
b = g.p.screen.image.convert('RGB').copy()
s = Image.new('RGB', (320, 144)); s.paste(a, (0, 0)); s.paste(b, (160, 0))
s.resize((960, 432), Image.NEAREST).save('shots/t_conn2.png')
g.close()
