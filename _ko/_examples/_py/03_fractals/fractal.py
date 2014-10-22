import decodes
from decodes.core import *
outie = decodes.make_out(decodes.Outies.Rhino)

from math import *

"""
A Monster as Input
"""
aa = 5.0
bb = 1.5

def evaluate(t):
    x = (aa-bb)*math.cos(t) + bb*cos(t*((aa/bb)-1))
    y = (aa-bb)*math.sin(t) + bb*sin(t*((aa/bb)-1))
    return Point(x,y)
     
cnt = 10  
#seed_pts = [evaluate(t) for t in Interval(0, 2*pi).divide(cnt, True)]

"""
Any Collection of Lines as Input
"""
seed_pts = [Point(5*cos(t), 7*sin(t)**2) for t in Interval(0, 2*pi)/10]


seed_lines = [Segment(seed_pts[n], seed_pts[n+1]) for n in range(9)]
steps = 5

"""
Fractal
Generates a Koch Fractal on a collection of line segments
"""

divs = ( 0 , 1/3 , 0.5 , 2/3 , 1 )
height_ratio = 1/3

for step in range(steps):
    new_lines = []
    for line in seed_lines:
        height = line.length*height_ratio
        pts = [line.eval(t) for t in divs]
        vec = line.vec.cross(Vec(0,0,1)).normalized(height)
        pts[2] += vec
        new_lines.extend( [Segment(pts[n],pts[n+1]) for n in range(len(pts)-1)] )
    seed_lines = new_lines

outie.put(new_lines)

outie.draw()
