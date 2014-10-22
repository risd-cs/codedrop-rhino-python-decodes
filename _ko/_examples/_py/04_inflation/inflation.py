import decodes
from decodes.core import *
outie = decodes.make_out(decodes.Outies.Rhino)


"""
Regular Polygon as Input
"""
center = Point(10,0)
pgon =RGon(basis= CS(center), num_of_sides=5, radius=5)

steps = 5
t = 0.2

"""
Inflation
"""
for n in range(steps):
    pts = []
    for line in pgon.edges:
        pts.append(line.eval(t))
    new_pgon = PGon(pts)
    outie.put(new_pgon)
    pgon = new_pgon


outie.draw()
