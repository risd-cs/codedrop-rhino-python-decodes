import decodes
from decodes.core import *

# vector construction 
pt_a = Point()
pt_b = Point(-2,4,5)
vec_a = Vec(0,2,0)
vec_b = Vec(pt_a,pt_b)

print vec_b.length

# point-vector interaction
pt_c = Point(2,3,-1)
pt_d = pt_c + vec_a
print pt_d


#note: vectors are not drawn;  one can write methods to do so