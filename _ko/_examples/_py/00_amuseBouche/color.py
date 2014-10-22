import decodes
from decodes.core import *

r,g,b = 1.0, 0.5, 0.5

pt_a = Point()
vec_a = Vec(10,10,10)
ln_a = Segment(pt_a, vec_a)
ln_a.set_color(r,g,b)

outie = decodes.make_out(decodes.Outies.Rhino)
outie.put(ln_a)  

outie.draw()