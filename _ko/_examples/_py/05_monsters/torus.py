import decodes
from decodes.core import *
outie = decodes.make_out(decodes.Outies.Rhino)

from math import *

r = 3.0 #minor radius
R = 4.5 #major radius

def torus(u,v):
    x = (R + r*cos(v))*cos(u)
    y = (R + r*cos(v))*sin(u)
    z = r*sin(v)
    return Point(x,y,z)

surf = Surface(torus, Interval.twopi(), Interval.twopi())

outie.put(surf.surrogate)




outie.draw()
