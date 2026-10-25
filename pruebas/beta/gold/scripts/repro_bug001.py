"""BUG-001 visual repro: ROUTE_29 -> NEW_BARK_TOWN on foot, open+close the bag (RefreshSprites), walk to the Teacher.
Compares with the control run where the bag is not opened. Writes shots/BUG001_control.png and shots/BUG001_bug.png."""
from lib import *
arm(400)
def run(open_bag, label):
    g = G('ROUTE_29', 57, 9, hour=12)
    g.p.tick(60)
    for i in range(9):
        g.press('right', 4, hold=16)
        if where(g)[0] == 'NEW_BARK_TOWN': break
    g.p.tick(60)
    if open_bag: pack_cycle(g)
    for i in range(5): g.press('right', 4, hold=16)
    g.p.tick(60)
    print(label, where(g), objs_in_view(g), check_objects(g))
    im = g.p.screen.image.convert('RGB').resize((480, 432), Image.NEAREST)
    im.save('shots/BUG001_%s.png' % label)
    g.close()
    return im
a = run(False, 'control'); b = run(True, 'bug')
s = Image.new('RGB', (960, 432)); s.paste(a, (0, 0)); s.paste(b, (480, 0)); s.save('shots/BUG001_side_by_side.png')
