Usage Patterns
==============

MUMPS Job Lifecycle
-------------------

PyMUMPS wraps MUMPS jobs with ``ctx.run(job=...)``:

- ``job=1``: analysis
- ``job=2``: factorization
- ``job=3``: solve
- ``job=4``: analysis + factorization
- ``job=5``: factorization + solve
- ``job=6``: analysis + factorization + solve

When reusing a matrix structure for multiple right-hand sides, a common pattern is:

1. run analysis once,
2. factorize once (or when values change),
3. solve repeatedly.

Centralized Matrix Input
------------------------

With centralized assembly, rank 0 provides the full sparse matrix:

.. code-block:: python

   from mumps import DMumpsContext

   ctx = DMumpsContext()
   if ctx.myid == 0:
       ctx.set_centralized_sparse(A)
       x = b.copy()
       ctx.set_rhs(x)

   ctx.run(job=6)
   ctx.destroy()

``set_centralized_sparse`` accepts SciPy sparse matrices and converts to COO internally.

Distributed Matrix Input
------------------------

For distributed assembled matrices, each rank sets its local entries:

.. code-block:: python

   ctx.set_icntl(18, 3)  # enable distributed assembled input mode
   ctx.set_distributed_assembled(irn_loc, jcn_loc, a_loc)

Use one-based indices when providing ``irn`` and ``jcn`` arrays.

Sparse Right-Hand Side
----------------------

To provide sparse RHS data:

.. code-block:: python

   rhs_storage = ctx.set_rhs_centralized_sparse(rhs_sparse)
   ctx.run(job=3)

This activates the relevant MUMPS sparse-RHS control internally.

Determinant Computation
-----------------------

High-level ``factorize`` can compute determinants by enabling ``icntl(33)`` before factorization:

.. code-block:: python

   solver = mumps.factorize(A, options={"det": True})
   det_a = solver.det

Determinant is returned only on rank 0.

Data Types
----------

PyMUMPS supports:

- ``float32`` via ``SMumpsContext``
- ``float64`` via ``DMumpsContext``
- ``complex64`` via ``CMumpsContext``
- ``complex128`` via ``ZMumpsContext``

Use matching ``A.dtype`` and ``b.dtype`` with ``mumps.spsolve``.
