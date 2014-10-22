import decodes
from decodes.core import *
outie = decodes.make_out(decodes.Outies.Rhino)

seg_a = Segment(Point(0,2), Point(10,5))
seg_b = Segment(Point(0,-2), Point(10,3))
outie.put(seg_a)
outie.put(seg_b)

hump_count = 3
chain_count = 3

"""
Guilloche
Generates a set of overlapping chains between two line segments
"""

chains = []
res = 30
twopi = Interval.twopi()
for n in range(chain_count):
    t = (n/chain_count)
    pts = []
    off = (math.pi * 2 / hump_count) * t
    for y in Interval().divide(res,True):
        pt_a = seg_a.eval(y)
        pt_b = seg_b.eval(y)
        theta = twopi.eval(y)+off
        tt = (1.0 + math.sin(theta*hump_count))/2
        pts.append(Point.interpolate(pt_a,pt_b,tt))
    chain = []
    for n in range(len(pts)-1): chain.append(Segment(pts[n],pts[n+1]))
    chains.append(chain)
    
outie.put(chains)

outie.draw()
