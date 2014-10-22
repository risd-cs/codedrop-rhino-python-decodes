import decodes
from decodes.core import *
outie = decodes.make_out(decodes.Outies.Rhino)

seg_a = Segment(Point(0,2), Point(10,5))
seg_b = Segment(Point(0,-2), Point(10,3))
outie.put(seg_a)
outie.put(seg_b)

hump_count = 6

"""
Guilloche
Generates a set of overlapping chains between two line segments
"""

res = 50
t = 0.2
pts = []
off = (math.pi * 2 / hump_count) * t
twopi = Interval.twopi()
for y in Interval().divide(res,True):
    pt_a = seg_a.eval(y)
    pt_b = seg_b.eval(y)
    theta = twopi.eval(y)+off
    tt = (1.0 + math.sin(theta*hump_count))/2
    pts.append(Point.interpolate(pt_a,pt_b,tt))
    
chain = []
for n in range(len(pts)-1): 
    chain.append(Segment(pts[n],pts[n+1]))

outie.put(chain)

outie.draw()
