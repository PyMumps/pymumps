PyMUMPS: A parallel sparse direct solver
=========================================


Requirements
------------

* [MUMPS](https://mumps-solver.org/)
* [mpi4py](https://code.google.com/p/mpi4py/)


Installation
------------

If necessary define `LIBRARY_PATH` and `C_INCLUDE_PATH` before running the next steps.

PyMUMPS can be installed from PyPI using pip:

```
pip install pymumps
```

Custom build flags, e.g. to specify the MUMPS installation location,
can be specified using `-C`:

```
pip install -v \
    -Cbuild.verbose=true \
    -Ccmake.define.MUMPS_ROOT=<PATH_OF_MUMPS_INSTALLATION> \
    pymumps
```

There is also conda recipe:

```
conda install -c conda-forge pymumps
```


Test if pyMUMPS is installed
------------

Test the obtained installation using

    python -c "import mumps"

or run tests using (`pytest`is required) after installing pymumps

    pytest --pyargs mumps


Examples
--------

Centralized input & output. The sparse matrix and right hand side are
input only on the rank 0 process. The system is solved using all
available processes and the result is available on the rank 0 process.

```python
from mumps import DMumpsContext
ctx = DMumpsContext()
if ctx.myid == 0:
    ctx.set_centralized_sparse(A)
    x = b.copy()
    ctx.set_rhs(x) # Modified in place
ctx.run(job=6) # Analysis + Factorization + Solve
ctx.destroy() # Cleanup
```

Re-use symbolic or numeric factorizations.

```python
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
```

Use `spsolve` function

```python
import numpy as np
import scipy.sparse as sp
import mumps

# test data
dataIRN = np.array([1, 2, 4, 5, 2, 1, 5, 3, 2, 3, 1, 3], dtype=np.int32)
dataJCN = np.array([2, 3, 3, 5, 1, 1, 2, 4, 5, 2, 3, 3], dtype=np.int32)
dataVAL = np.array([3.0, -3.0, 2.0, 1.0, 3.0, 2.0, 4.0, 2.0, 6.0, -1.0, 4.0, 1.0], dtype=np.float64)
dataRHS = np.array([20.0, 24.0, 9.0, 6.0, 13.0], dtype=np.float64)

# build sparse matrix
A = sp.coo_matrix((dataVAL, (dataIRN - 1, dataJCN - 1)), shape=(5, 5))

sol = mumps.spsolve(A, dataRHS)
```

Use `factorize` to solve multiple right-hand sides efficiently

```python
import numpy as np
import scipy.sparse as sp
import mumps

# test data
dataIRN = np.array([1, 2, 4, 5, 2, 1, 5, 3, 2, 3, 1, 3], dtype=np.int32)
dataJCN = np.array([2, 3, 3, 5, 1, 1, 2, 4, 5, 2, 3, 3], dtype=np.int32)
dataVAL = np.array([3.0, -3.0, 2.0, 1.0, 3.0, 2.0, 4.0, 2.0, 6.0, -1.0, 4.0, 1.0], dtype=np.float64)

# build sparse matrix
A = sp.coo_matrix((dataVAL, (dataIRN - 1, dataJCN - 1)), shape=(5, 5))

# factorize once (determinant computation enabled by default)
obj = mumps.factorize(A)

# solve for the first right-hand side
rhs1 = np.array([20.0, 24.0, 9.0, 6.0, 13.0], dtype=np.float64)
sol1 = obj.solve(rhs1)  # [1., 2., 3., 4., 5.] on rank 0, None elsewhere

# reuse the same factorization for a second right-hand side
rhs2 = np.array([4.0, 7.0, 0.0, 4.0, 9.0], dtype=np.float64)
sol2 = obj.solve(rhs2)

# solve for multiple right-hand sides at once
rhs_multi = np.stack([rhs1, rhs2])        # shape (2, 5)
sol_multi  = obj.solve(rhs_multi)         # shape (2, 5) on rank 0

obj.destroy()
```

Compute the determinant of a sparse matrix

```python
import numpy as np
import scipy.sparse as sp
import mumps

# build sparse matrix
dataIRN = np.array([1, 2, 4, 5, 2, 1, 5, 3, 2, 3, 1, 3], dtype=np.int32)
dataJCN = np.array([2, 3, 3, 5, 1, 1, 2, 4, 5, 2, 3, 3], dtype=np.int32)
dataVAL = np.array([3.0, -3.0, 2.0, 1.0, 3.0, 2.0, 4.0, 2.0, 6.0, -1.0, 4.0, 1.0], dtype=np.float64)
A = sp.coo_matrix((dataVAL, (dataIRN - 1, dataJCN - 1)), shape=(5, 5))

# factorize with determinant computation enabled (default: True)
obj = mumps.factorize(A, options={"det": True})

# retrieve the determinant (available on rank 0, None on other ranks)
det = obj.det   # 228.0
obj.destroy()
```

