import decodes
from decodes.core import *
outie = decodes.make_out(decodes.Outies.Rhino)

vec_a = Vec(0,0,5)
pt_a = Point(2,3)
ln_a = Segment(pt_a, vec_a)
ln_a.set_color(1,0,0)
ln_a.set_weight(5)
outie.put(ln_a)

outie.draw()
