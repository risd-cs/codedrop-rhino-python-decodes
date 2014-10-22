do_it = True
if do_it:
    print "it's done."
    
    
if 1+1 > 2:
    print "Albers was right!"
else:
    print "Albers was wrong!"

#a geometric example

import decodes
from decodes.core import *

vec_a = Vec(1,0,0)
vec_b = Vec(2,1,3)
if vec_a.dot(vec_b) == 0:
    print "Vectors are perpendicular"
else:
    print "Vectors aren't perpendicular"