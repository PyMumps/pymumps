import numpy as np
import mumps
import pytest


@pytest.fixture
def matrix():
    # Set up the test problem:
    n = 5
    irn = np.array([1, 2, 4, 5, 2, 1, 5, 3, 2, 3, 1, 3], dtype="i")
    jcn = np.array([2, 3, 3, 5, 1, 1, 2, 4, 5, 2, 3, 3], dtype="i")
    a = np.array([3.0, -3.0, 2.0, 1.0, 3.0, 2.0, 4.0, 2.0, 6.0, -1.0, 4.0, 1.0], dtype="d")

    return (n, a, irn, jcn)


@pytest.fixture
def rhs():
    b = np.array([20.0, 24.0, 9.0, 6.0, 13.0], dtype="d")

    return b


def test_solve(matrix, rhs):
    b = rhs
    (n, a, irn, jcn) = matrix

    # Create the MUMPS context and set the array and right hand side
    with mumps.DMumpsContext(sym=0, par=1) as ctx:
        if ctx.myid == 0:
            ctx.set_shape(n)
            ctx.set_centralized_assembled(irn, jcn, a)
            x = b.copy()
            ctx.set_rhs(x)

        ctx.set_silent()  # Turn off verbose output

        ctx.run(job=6)  # Analysis + Factorization + Solve

        assert np.allclose(x, np.arange(1, 6))


def test_solve_complex(matrix, rhs):
    b = rhs + rhs * 2j
    (n, a, irn, jcn) = matrix
    a = a.astype("D")

    # Create the MUMPS context and set the array and right hand side
    with mumps.ZMumpsContext(sym=0, par=1) as ctx:
        if ctx.myid == 0:
            ctx.set_shape(n)
            ctx.set_centralized_assembled(irn, jcn, a)
            x = b.copy()
            ctx.set_rhs(x)

        ctx.set_silent() # Turn off verbose output

        ctx.run(job=6) # Analysis + Factorization + Solve

        assert np.allclose(x, np.arange(1, 6) + np.arange(1, 6) * 2j)
