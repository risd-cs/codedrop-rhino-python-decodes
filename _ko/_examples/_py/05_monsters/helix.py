import decodes
from decodes.core import *
outie = decodes.make_out(decodes.Outies.Rhino)


from math import *
#helical curve defined by a freeform profile (a 3 pt Bezier) 

height = 28
rad_cap = 6.2
rad_mid = -2.9
mid_height = 0.7
turns = 6
k = 2

def point_by_cyl_coords(radius,radians,z):
    x = radius * math.cos(radians)
    y = radius * math.sin(radians)
    return Point(x,y,z)

def func_rad(t):
    pt_a = Point(rad_cap,0)
    pt_b = Point(rad_mid,mid_height*height)
    pt_c = Point(rad_cap,height)
    rad = Curve.bezier([pt_a,pt_b,pt_c]).eval(t/height).x
    return rad
 
def func_theta(t):
    theta = 2*turns*pi*(t/height)**k
    return theta

def func_helix(t):
    rad = func_rad(t)
    theta = func_theta(t)
    return point_by_cyl_coords(rad, theta, t)

ival = Interval(0,height)
crv = Curve(func_helix, ival, height/100)

outie.put(crv.surrogate)
outie.draw()
