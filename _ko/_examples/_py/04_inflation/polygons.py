import decodes
from decodes.core import *
outie = decodes.make_out(decodes.Outies.Rhino)

"""
More Shapes:  Polygons, Stock Polygons (Rectangle, Doughnut), Regular Polygons
"""


# basic polygon construction
pts_a = [Point(-10,0),Point(-8,1),Point(-6,0),Point(-8,-1)]
my_pgon = PGon(pts_a)
outie.put(my_pgon)

# rectangle construction
center = Point(-5,0)
width = 2
height = 5
rect = PGon.rectangle(center, width, height)
outie.put(rect)


#regular polygons - can be constructed by specifying edge length, apothem 
#(distance from center midpoint of edge or radius (distance from 
#center to a vertex) 

sides = 5
edge = 2
apoth = 3
rad = 5

#if no center is specified this defaults to a center of (0,0,0)
my_rgon=RGon(num_of_sides=sides, edge_length=edge)

center = Point(5,0)
my_rgon2=RGon(basis = CS(center), num_of_sides=sides, apothem=apoth)

center +=Vec(10,0)
my_rgon3 = RGon(basis = CS(center), num_of_sides = sides, radius = rad)

outie.put(my_rgon)
outie.put(my_rgon2)
outie.put(my_rgon3)


#some polygon properties
#sides can be accessed by index 
print rect.edges[1]
#points along sides can be accessed using eval
print rect.edges[1].eval(0.5)



outie.draw()