Context Classes
===============

PyMUMPS provides four data-type specific context classes.

.. py:class:: mumps.DMumpsContext(par=1, sym=0, comm=None, del_warning=True)

   Double-precision real MUMPS context (float64).

.. py:class:: mumps.SMumpsContext(par=1, sym=0, comm=None, del_warning=True)

   Single-precision real MUMPS context (float32).

.. py:class:: mumps.CMumpsContext(par=1, sym=0, comm=None, del_warning=True)

   Single-precision complex MUMPS context (complex64).

.. py:class:: mumps.ZMumpsContext(par=1, sym=0, comm=None, del_warning=True)

   Double-precision complex MUMPS context (complex128).

Shared Interface
----------------

All four classes expose the same operational methods through a shared
base implementation. See :doc:`mumps_base` for the full method reference.
