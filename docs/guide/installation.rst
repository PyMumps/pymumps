Installation
============

Requirements
------------

PyMUMPS requires:

- Python 3.8+
- a working MUMPS installation
- ``mpi4py`` and an MPI runtime

Install From PyPI
-----------------

.. code-block:: bash

   pip install pymumps

Install With Explicit MUMPS Location
------------------------------------

If MUMPS is not in standard system paths, pass build configuration to pip:

.. code-block:: bash

   pip install -v \
     -Cbuild.verbose=true \
     -Ccmake.define.MUMPS_ROOT=/path/to/mumps \
     pymumps

Install From Conda-Forge
------------------------

.. code-block:: bash

   conda install -c conda-forge pymumps

Developer Installation
----------------------

From a local checkout:

.. code-block:: bash

   pip install -v -Ccmake.define.MUMPS_ROOT=${CONDA_PREFIX} -e .[test]

Validation
----------

Check import:

.. code-block:: bash

   python -c "import mumps"

Run tests:

.. code-block:: bash

   pytest --pyargs mumps

For MPI-enabled environments:

.. code-block:: bash

   mpirun -n 2 pytest
