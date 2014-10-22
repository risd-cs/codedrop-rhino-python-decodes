import decodes
from decodes.core import *

# segment construction
#  by point-vec
pt_a = Point(-2,5,0)
ln_a = Segment(pt_a, Vec(2,1,0))
#  by 2 points
pt_b = Point(5,-10,10)
ln_b = Segment(pt_a, pt_b)

print "segment start point is", ln_b.spt
print "segment end point is", ln_b.ept
ln_b = ln_b.inverted()
print "segment start point is now", ln_b.spt
print "segment end point is now", ln_b.ept
print "segment midpoint is", ln_b.midpoint
print "segment length is ", ln_b.length
t = 0.25
pt_at_t = ln_b.eval(t) #t represents the fraction of the segment length


outie = decodes.make_out(decodes.Outies.Rhino)
outie.put(ln_b)
outie.put(pt_at_t)

outie.draw()