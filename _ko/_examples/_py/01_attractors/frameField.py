import decodes
from decodes.core import *
outie = decodes.make_out(decodes.Outies.Rhino)

"""
Grid #2 as Input
"""
canvas_x = 14 #length of side in horizontal "x" direction
canvas_y = 14 #length of side in vertical "y" direction
cnt_x = 10 #number of grid points in "x" direction
cnt_y = 12 #number of grid points in "y" direction
pts = [Point(i*canvas_x/cnt_x, j*canvas_y/cnt_y) for i in range(cnt_x) for j in range(cnt_y)]

attr_pt = Point(8,8)

"""
A Frame Field
This script generates a field of frames at each input grid point 
with orientation dependent on an attractor point
"""
x_rays, y_rays = [],[]
for pt in pts:
    vec_x = Vec(pt,attr_pt).normalized(0.6)
    vec_y = vec_x.cross(Vec(0,0,1)).normalized(0.6) #this will give a perpendicular vector
    
    x_rays.append(Segment(pt,vec_x))
    y_rays.append(Segment(pt,vec_y))
    
outie = decodes.make_out(decodes.Outies.Rhino)
outie.put(x_rays)
outie.put(y_rays)
outie.draw()
