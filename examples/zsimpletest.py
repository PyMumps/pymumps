"""
ZMUMPS test routine.

Run as:
    mpirun -np 2 python zsimpletest.py
or
    mpiexec -np 2 python zsimpletest.py

The solution should be

  -0.0020 + 0.0078j
  -0.0067 + 0.0066j
  -0.0087 + 0.0028j
  -0.0073 - 0.0022j
  -0.0029 - 0.0063j
   0.0027 - 0.0079j
  -0.0029 - 0.0063j
  -0.0073 - 0.0022j
  -0.0087 + 0.0028j
  -0.0067 + 0.0066j
  -0.0020 + 0.0078j
"""

import numpy as np
import mumps

# Set up the test problem:
# irn and jcn are 1-based, not 0-based
n = 11
irn = np.array([1      ,1 ,2 ,2   ,2 ,3 ,3   ,3 ,4 ,4   ,4 ,5 ,5   ,5 ,6 ,6   ,6 ,7 ,7   ,7 ,8 ,8   ,8 ,9 ,9   ,9 ,10,10  ,10,11 ,11    ], dtype='i')
jcn = np.array([1      ,2 ,1 ,2   ,3 ,2 ,3   ,4 ,3 ,4   ,5 ,4 ,5   ,6 ,5 ,6   ,7 ,6 ,7   ,8 ,7 ,8   ,9 ,8 ,9   ,10,9 ,10  ,11,10 ,11    ], dtype='i')
a   = np.array([-1.-.6j,1.,1.,-1.6,1.,1.,-1.6,1.,1.,-1.6,1.,1.,-1.6,1.,1.,-1.6,1.,1.,-1.6,1.,1.,-1.6,1.,1.,-1.6,1.,1.,-1.6,1.,-1.,1.+.6j], dtype='D')
b = np.array([0.,0.,0.,0.,0.,-.01,0.,0.,0.,0.,0.], dtype='D')

# Create the MUMPS context and set the array and right hand side
ctx = mumps.ZMumpsContext(sym=0, par=1)
if ctx.myid == 0:
    ctx.set_shape(n)
    ctx.set_centralized_assembled(irn, jcn, a)
    x = b.copy()
    ctx.set_rhs(x)

ctx.set_silent() # Turn off verbose output

ctx.run(job=6) # Analysis + Factorization + Solve

if ctx.myid == 0:
    print("Solution is %s." % (x,))

ctx.destroy() # Free memory
