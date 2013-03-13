PyMUMPS: A parallel sparse direct solver
========================================

Requirements
------------

* [MUMPS](http://graal.ens-lyon.fr/MUMPS/)
* [mpi4py](https://code.google.com/p/mpi4py/)

Getting Started
---------------

Install using `python setup.py install` or run from the local checkout.

Examples
--------

Centralized input & output. The sparse matrix and right hand side are
input only on the rank 0 process. The system is solved using all
available processes and the result is available on the rank 0 process.

    from mumps import DMumpsContext
    ctx = DMumpsContext()
    if ctx.myid == 0:
        ctx.set_centralized_sparse(A)
        x = b.copy()
        ctx.set_rhs(x) # Modified in place
    ctx.run(job=6) # Analysis + Factorization + Solve
    ctx.destroy() # Cleanup

Re-use symbolic or numeric factorizations.

    from mumps import DMumpsContext
    ctx = DMumpsContext()
    if ctx.myid == 0:
        ctx.set_centralized_assembled_rows_cols(A.row+1, A.col+1) # 1-based
    ctx.run(job=1) # Analysis

    if ctx.myid == 0:
        ctx.set_centralized_assembled_values(A.data)
    ctx.run(job=2) # Factorization

    if ctx.myid == 0:
        x = b1.copy()
        ctx.set_rhs(x)
    ctx.run(job=3) # Solve

    # Reuse factorizations by running `job=3` with new right hand sides
    # or analyses by supplying new values and running `job=2` to repeat
    # the factorization process.
