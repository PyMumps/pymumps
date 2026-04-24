High-Level API
==============

.. py:function:: mumps.spsolve(A, b, comm=None)

   Solve A x = b for sparse matrix A and right-hand side b.

   Parameters
      A: scipy.sparse matrix in compatible dtype.
      b: dense or sparse right-hand side with matching dtype.
      comm: optional mpi4py communicator.

   Returns
      Rank 0: solution array.
      Other ranks: None.

   Notes
      Supported dtypes are float32, float64, complex64, and complex128.

.. py:class:: mumps.factorize(A=None, comm=None, options={'det': True})

   High-level reusable factorization wrapper.

   The matrix is analyzed and factorized at construction time, then reused
   for repeated solve calls.

.. py:method:: mumps.factorize.set_matrix(matrix)

   Set the matrix to be factorized (rank 0 workflow).

.. py:method:: mumps.factorize.set_rhs(rhs=None)

   Set right-hand side for the next solve call.

.. py:method:: mumps.factorize.solve(b=None)

   Solve using existing factorization.

   Returns the solution on rank 0 and None on other ranks.

.. py:method:: mumps.factorize.destroy()

   Release MUMPS resources for this factorization object.

.. py:property:: mumps.factorize.det

   Determinant value when enabled with option det=True.

   Available on rank 0 only.
