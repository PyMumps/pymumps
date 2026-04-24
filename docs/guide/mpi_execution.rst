MPI Execution Model
===================

PyMUMPS is designed for MPI execution through ``mpi4py``.

Key Behavior
------------

- By default, contexts use ``MPI.COMM_WORLD``.
- Rank 0 usually supplies centralized matrix and RHS data.
- Solve outputs are returned on rank 0 only; other ranks receive ``None`` from high-level helpers.

Run Scripts With MPI
--------------------

.. code-block:: bash

   mpirun -n 2 python examples/dsimpletest.py

Run Test Suite With MPI
-----------------------

.. code-block:: bash

   mpirun -n 2 pytest

Custom Communicators
--------------------

You can pass any ``mpi4py`` communicator:

.. code-block:: python

   from mpi4py import MPI
   from mumps import DMumpsContext

   subcomm = MPI.COMM_WORLD.Split(color=0, key=MPI.COMM_WORLD.rank)
   ctx = DMumpsContext(comm=subcomm)

The communicator must remain valid for the lifetime of the context.

Resource Cleanup
----------------

Always release MUMPS internal resources:

.. code-block:: python

   ctx.destroy()

or use context manager style for helper APIs that support it.
