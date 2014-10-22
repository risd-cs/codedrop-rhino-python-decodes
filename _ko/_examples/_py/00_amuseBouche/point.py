import decodes
from decodes.core import *


"""
Point
"""
# point construction
pt_a = Point(2,3)
pt_b = Point(10,20,30)
print pt_a
print pt_b

#dot operator accesses properties and methods
print pt_a.x, pt_a.y, pt_a.z
print pt_a.distance(pt_b)


# point manipulation
pt_a.x = 3
print pt_a


"""
Drawing Geometry
"""
outie = decodes.make_out(decodes.Outies.Rhino)  #this contains the geometry to be drawn
outie.put(pt_a)
outie.put(pt_b)
outie.draw()