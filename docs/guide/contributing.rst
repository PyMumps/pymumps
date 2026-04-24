Contributing
============

Development Setup
-----------------

1. Clone the repository.
2. Prepare an environment with Python, MPI, and MUMPS.
3. Install in editable mode with test dependencies.

.. code-block:: bash

   pip install -v -Ccmake.define.MUMPS_ROOT=${CONDA_PREFIX} -e .[test]

Run Tests
---------

Local tests:

.. code-block:: bash

   python -m pytest

MPI tests:

.. code-block:: bash

   mpirun -n 2 pytest

Code Style And Quality
----------------------

This project defines formatting and linting-related tooling in ``pyproject.toml``.
Please keep contributions consistent with existing style.

Documentation
-------------

Build docs locally:

.. code-block:: bash

   pip install -r docs/requirements.txt
   sphinx-build -b html docs docs/_build/html

Pull Requests
-------------

Include in your PR:

- tests for behavioral changes,
- documentation updates for user-facing changes,
- a concise summary of the motivation and impact.
