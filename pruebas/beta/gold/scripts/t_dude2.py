from lib import *
arm(500)
g = G('ROUTE_29', 55, 9)
g.write('wRoute29SceneID', 1)
g.p.tick(60)
g.p.button_press('left')
frames=[]
for i in range(130):
    g.p.tick(2)
    if i == 40: g.p.button_release('left')
    if 70 <= i <= 100 and i % 3 == 0:
        frames.append((i, g.p.screen.image.convert('RGB').copy(), safe(g), oam_check(g)))
W=160
s = Image.new('RGB', (W*5, 144*((len(frames)+4)//5)))
for k,(i,im,sf,b) in enumerate(frames):
    s.paste(im, ((k%5)*W, (k//5)*144)); print(i, sf, len(b))
s.resize((s.width*2, s.height*2), Image.NEAREST).save('shots/dude_seq.png')
g.close()
