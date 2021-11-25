import numpy as np
import numpy.linalg as LA

b = np.array([[2, 5],[3, -8]])
w,v = LA.eig(b)
print(w)
print(v)
print(v.T)