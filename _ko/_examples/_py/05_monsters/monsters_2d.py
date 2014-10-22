import decodes
from decodes.core import *
outie = decodes.make_out(decodes.Outies.Rhino)

from math import *

aa = 5.0
bb = 1.5
cnt = 50

"""
Monsters, reworked as a decodes curve
"""

def func(t):
    x = (aa-bb)*math.cos(t) + bb*cos(t*((aa/bb)-1))
    y = (aa-bb)*math.sin(t) + bb*sin(t*((aa/bb)-1))
    return Point(x,y)

ival = Interval(0,2*pi)
tol = ival.delta/cnt
crv = Curve(func,ival,tol)

outie.put(crv.surrogate)



outie.draw()
