Low-Level Context Interface
===========================

The methods below are shared by all context variants.

Lifecycle And Execution
-----------------------

.. py:method:: _MumpsBaseContext.run(job)

   Set the job code and execute MUMPS.

.. py:method:: _MumpsBaseContext.set_job(job)

   Set the MUMPS job code without running.

.. py:method:: _MumpsBaseContext.mumps()

   Execute MUMPS and raise runtime error on negative global info code.

.. py:method:: _MumpsBaseContext.destroy()

   Finalize MUMPS context and release held array references.

.. py:property:: _MumpsBaseContext.destroyed

   True if the context has already been destroyed.

Matrix Assembly
---------------

.. py:method:: _MumpsBaseContext.set_shape(n)

.. py:method:: _MumpsBaseContext.set_centralized_sparse(A)

.. py:method:: _MumpsBaseContext.set_centralized_assembled(irn, jcn, a)

.. py:method:: _MumpsBaseContext.set_centralized_assembled_rows_cols(irn, jcn)

.. py:method:: _MumpsBaseContext.set_centralized_assembled_values(a)

.. py:method:: _MumpsBaseContext.set_distributed_assembled(irn_loc, jcn_loc, a_loc)

.. py:method:: _MumpsBaseContext.set_distributed_assembled_rows_cols(irn_loc, jcn_loc)

.. py:method:: _MumpsBaseContext.set_distributed_assembled_values(a_loc)

Right-Hand Side Handling
------------------------

.. py:method:: _MumpsBaseContext.set_rhs(rhs)

.. py:method:: _MumpsBaseContext.set_rhs_shape(nz_rhs, nrhs=1)

.. py:method:: _MumpsBaseContext.set_rhs_centralized_sparse(rhs)

.. py:method:: _MumpsBaseContext.allocate_rhs(lrhs, nrhs, rhs_dtype)

.. py:method:: _MumpsBaseContext.set_rhs_centralized_assembled(irhs_sparse, irhs_ptr, rhs_sparse)

.. py:method:: _MumpsBaseContext.set_rhs_centralized_assembled_ptr_indices(irhs_ptr, irhs_sparse)

.. py:method:: _MumpsBaseContext.set_rhs_centralized_assembled_values(rhs)

Solver Controls And Diagnostics
-------------------------------

.. py:method:: _MumpsBaseContext.set_icntl(idx, val)

.. py:method:: _MumpsBaseContext.get_icntl(idx)

.. py:method:: _MumpsBaseContext.set_cntl(idx, val)

.. py:method:: _MumpsBaseContext.get_cntl(idx)

.. py:method:: _MumpsBaseContext.get_info(idx)

.. py:method:: _MumpsBaseContext.get_infog(idx)

.. py:method:: _MumpsBaseContext.get_rinfo(idx)

.. py:method:: _MumpsBaseContext.get_rinfog(idx)

.. py:method:: _MumpsBaseContext.set_silent()

Sparse RHS Controls
-------------------

.. py:method:: _MumpsBaseContext.set_rhs_sparse_mode(mode=1)

.. py:method:: _MumpsBaseContext.set_rhs_sparse_deactive()

Utilities
---------

.. py:method:: _MumpsBaseContext.cast_array(arr)

   Static helper converting a NumPy array to a C-level pointer address.

