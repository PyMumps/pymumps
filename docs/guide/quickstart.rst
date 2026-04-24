Quickstart
==========

Solve A x = b In One Call
-------------------------

.. code-block:: python

   import numpy as np
   import scipy.sparse as sp
   import mumps

   irn = np.array([1, 2, 4, 5, 2, 1, 5, 3, 2, 3, 1, 3], dtype=np.int32)
   jcn = np.array([2, 3, 3, 5, 1, 1, 2, 4, 5, 2, 3, 3], dtype=np.int32)
   val = np.array([3.0, -3.0, 2.0, 1.0, 3.0, 2.0, 4.0, 2.0, 6.0, -1.0, 4.0, 1.0], dtype=np.float64)
   rhs = np.array([20.0, 24.0, 9.0, 6.0, 13.0], dtype=np.float64)

   A = sp.coo_matrix((val, (irn - 1, jcn - 1)), shape=(5, 5))
   x = mumps.spsolve(A, rhs)

On MPI rank 0, ``x`` contains the solution. On other ranks, the return value is ``None``.

Reuse A Factorization For Multiple Right-Hand Sides
---------------------------------------------------

.. code-block:: python

   solver = mumps.factorize(A)

   x1 = solver.solve(rhs)
   rhs2 = np.array([4.0, 7.0, 0.0, 4.0, 9.0], dtype=np.float64)
   x2 = solver.solve(rhs2)

   # Determinant is available by default (rank 0 only)
   det_a = solver.det

   solver.destroy()

Use Low-Level Context API
-------------------------

.. code-block:: python

   from mumps import DMumpsContext

   ctx = DMumpsContext(par=1, sym=0)
   if ctx.myid == 0:
       ctx.set_centralized_sparse(A)
       x = rhs.copy()
       ctx.set_rhs(x)

   ctx.set_silent()
   ctx.run(job=6)  # analysis + factorization + solve
   ctx.destroy()

``job=6`` performs the full solve pipeline. See :doc:`usage_patterns` for full job sequencing.
