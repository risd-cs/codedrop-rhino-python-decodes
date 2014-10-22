import decodes
from decodes.core import *
outie = decodes.make_out(decodes.Outies.Rhino)

from math import *


line_in = Segment(Point(10,0), Point(-1,-5))

"""
Line Replacement Rule
Replaces a line with a collection of lines - this one is the basis for the Koch Fractal
"""

divs = ( 0 , 1/3 , 0.5 , 2/3 , 1 )
height_ratio = 1/3

height = line_in.length*height_ratio
pts = [line_in.eval(t) for t in divs]
vec = line_in.vec.cross(Vec(0,0,1)).normalized(height)
pts[2] += vec
new_lines = [Segment(pts[n],pts[n+1]) for n in range(len(pts)-1)] 
    
outie.put(new_lines)

outie.draw()
