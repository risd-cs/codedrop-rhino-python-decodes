count = 3
for n in range(count):
    print "n is equal to", n
    
    
for dictum in ["more." , "a bore."]:
    print "Less is", dictum

#a geometric example
import decodes
from decodes.core import *
outie = decodes.make_out(decodes.Outies.Rhino)

count = 5

pts = [Point(n, 2*n) for n in range(-count, count)]
#this is shorthand for the following code block
"""
pts = []
for n in range(-count, count):
    pts.append(Point(n, 2*n))
"""
    
outie.put(pts)

outie.draw()