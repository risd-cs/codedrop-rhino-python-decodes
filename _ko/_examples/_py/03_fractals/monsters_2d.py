import decodes
from decodes.core import *
outie = decodes.make_out(decodes.Outies.Rhino)

from math import *

aa = 5.0
bb = 1.5

"""
Monsters
A collection of points along a mathematical curve in 2D
"""

def evaluate(t):
    x = (aa-bb)*math.cos(t) + bb*cos(t*((aa/bb)-1))
    y = (aa-bb)*math.sin(t) + bb*sin(t*((aa/bb)-1))
    return Point(x,y)
     
cnt = 50   
pts = [evaluate(t) for t in Interval(0, 2*pi).divide(cnt, True)]
outie.put(pts)

pline = [Segment(pts[n], pts[n+1]) for n in range(cnt-1)]
outie.put(pline)


outie.draw()
