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
Inflation Routine Encapsulated as a Function
"""
def inflate(polygon, param):
    pts = [line.eval(param)for line in polygon.edges]
    return PGon(pts)

for n in range(steps):
    new_pgon = inflate(pgon, t)
    outie.put(new_pgon)
    pgon = new_pgon


outie.draw()
