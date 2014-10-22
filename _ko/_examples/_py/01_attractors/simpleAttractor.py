import decodes
from decodes.core import *
outie = decodes.make_out(decodes.Outies.Rhino)

"""
Grid #1
Generates a 2D grid of points spaced one unit apart
"""
pts = [Point(i, j) for i in range(-10, 10) for j in range(-10, 10)] 
attr_pt = Point(1,0)

"""
Another Simple Attractor Script
Moves points in a collection according to distance from an attractor point
"""
max_dist = 1
power = 0.3

for pt in pts: 
    # first, create a vector from 'pt' to the attractor point
    vec = Vec(pt,attr_pt)

    if vec.length > 0:
        # next, calculate the distance to move 'pt'
        dist = min(vec.length*max_dist,vec.length**power)
        # create a new point in the desired position
        new_pt = pt + vec.normalized(dist)
        outie.put(new_pt)


outie.draw()
