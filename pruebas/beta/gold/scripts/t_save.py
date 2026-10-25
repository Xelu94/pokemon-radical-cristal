"""Save through the in-game menu, restart the emulator with that SRAM and CONTINUE; check sprites. usage: t_save.py MAP x y [steps key]"""
import io, sys
import lib
from lib import *
arm(500)
name, x, y = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
ram = io.BytesIO(bytes(0x8000))
lib.RAM_FILE[0] = ram
g = G(name, x, y, hour=12)
strong_party(g)
g.p.tick(90)
print('before save', where(g), g.pos(), objs_in_view(g), check_objects(g))
g.press('start', 30)
for _ in range(3): g.press('down', 12)
g.press('a', 40)
for i in range(10):
    t = [r for r in screen_text2(g, range(12, 18)) if r.strip('│┌└┐┘─ ')]
    print(i, t)
    g.press('a', 80)
g.p.tick(200)
m = g.p.memory
m[0x0000] = 0x0A
chunks = []
for bank in range(4):
    m[0x4000] = bank
    chunks.append(bytes(m[0xA000:0xC000]))
data = b''.join(chunks)
print('sram bytes', len(data), 'nonzero', sum(1 for b in data if b))
g.p.stop(save=False)
ram2 = io.BytesIO(data)
lib.RAM_FILE[0] = ram2
g = G(name, x, y, init=False)   # continue: spawn patch is ignored, no re-init
g.p.tick(200)
for _ in range(4): g.press('a', 80)
g.p.tick(200)
print('after continue', where(g), g.pos(), objs_in_view(g), check_objects(g), 'party', g.read('wPartyCount'))
print('used', [(sprite_name(a), b) for a, b in used(g)][:8])
shot(g, 'continue_' + name)
g.close()
