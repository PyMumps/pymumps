import mumps
from scipy.sparse import coo_matrix, load_npz, tril
import numpy as np
import pdb

solver = mumps.DMumpsContext(sym=2, par=1)

matrix = load_npz('matrix.npz')
matrix = tril(matrix)
nrows, ncols = matrix.shape
assert nrows == ncols
dim = nrows

# These are the options used in my application
solver.set_icntl(13, 0)
solver.set_icntl(24, 0)
solver.set_icntl(11, 1)

solver.set_shape(dim)
solver.set_centralized_assembled_rows_cols(matrix.row+1, matrix.col+1)
solver.run(job=1)

solver.destroy()
