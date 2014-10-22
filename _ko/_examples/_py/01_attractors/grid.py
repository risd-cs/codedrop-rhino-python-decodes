import decodes
from decodes.core import *


"""
Grid #1
Generates a 2D grid of points spaced one unit apart
"""
pts_1 = [Point(i, j) for i in range(-10, 10) for j in range(-10, 10)]


"""
Grid #2
Generates a 2D grid of points anchored at origin with variable canvas size and grid count
"""
canvas_x = 14 #length of side in horizontal "x" direction
canvas_y = 14 #length of side in vertical "y" direction
cnt_x = 10 #number of grid points in "x" direction
cnt_y = 12 #number of grid points in "y" direction
pts_2 = [Point(i*canvas_x/cnt_x, j*canvas_y/cnt_y) for i in range(cnt_x) for j in range(cnt_y)]


outie = decodes.make_out(decodes.Outies.Rhino)
outie.put(pts_1)
#outie.put(pts_2)
outie.draw()
