FAQ
===

Why do I get import or build errors during installation?
---------------------------------------------------------

PyMUMPS requires a usable MUMPS installation and MPI toolchain at build time.
If MUMPS is installed in a custom location, pass:

.. code-block:: bash

   -Ccmake.define.MUMPS_ROOT=/path/to/mumps

Why does ``spsolve`` return ``None`` on some MPI ranks?
--------------------------------------------------------

This is expected. In centralized workflows, only rank 0 owns input and output arrays.

Can I reuse a factorization?
----------------------------

Yes. Use ``mumps.factorize(A)`` once and call ``solve`` repeatedly on new right-hand sides.

Do I have to call ``destroy()``?
--------------------------------

Yes, this is strongly recommended for predictable cleanup of MUMPS internals.

Which index base does MUMPS use?
--------------------------------

MUMPS expects one-based row and column indices. Convert from zero-based formats when needed.

How can I silence solver logs?
------------------------------

Use:

.. code-block:: python

   ctx.set_silent()
