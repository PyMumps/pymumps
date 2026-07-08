import numpy as np
import scipy as sp
import pytest
from mpi4py import MPI

comm = MPI.COMM_WORLD

mumps = pytest.importorskip("mumps")

# test data
dataIRN = [1, 2, 4, 5, 2, 1, 5, 3, 2, 3, 1, 3]
dataJCN = [2, 3, 3, 5, 1, 1, 2, 4, 5, 2, 3, 3]
dataVAL = [3.0, -3.0, 2.0, 1.0, 3.0, 2.0, 4.0, 2.0, 6.0, -1.0, 4.0, 1.0]
dataRHS = [20.0, 24.0, 9.0, 6.0, 13.0]
dataSOL = [1.0, 2.0, 3.0, 4.0, 5.0]

DATA_CASES = [
    ("mumps._cmumps", 'CMumpsContext', np.complex64, "complex64"),
    ("mumps._zmumps", 'ZMumpsContext', np.complex128, "complex128"),
    ("mumps._dmumps", 'DMumpsContext', np.float64, "real64"),
    ("mumps._smumps", 'SMumpsContext', np.float32, "real32"),
]

TEST_CASES = []
for data in DATA_CASES:
    module_name, context_cls_name, dtype, idcase = data
    if hasattr(mumps, context_cls_name):
        context_cls = getattr(mumps, context_cls_name)
        TEST_CASES.append((module_name, context_cls, dtype, idcase))



@pytest.fixture(params=TEST_CASES)
def mumps_case(request):
    module_name, context_cls, dtype, idcase = request.param
    pytest.importorskip(module_name)

    case = {
        "n": 5,
        "irn": np.array(dataIRN, dtype=np.int32),
        "jcn": np.array(dataJCN, dtype=np.int32),
        "aval": np.array(dataVAL, dtype=dtype),
        "rhs": np.array(dataRHS, dtype=dtype),
        "ctx": context_cls(par=1, sym=0, comm=comm),
        "dtype": dtype,
        "sol": np.array(dataSOL, dtype=dtype),
    }
    case["ctx"].set_silent()

    return case


def test_init(mumps_case):
    ctx = mumps_case["ctx"]
    if ctx.myid == 0:
        ctx.set_centralized_assembled(mumps_case["irn"], mumps_case["jcn"], mumps_case["aval"])
    ctx.destroy()
    assert ctx.destroyed


def test_rhs(mumps_case):
    ctx = mumps_case["ctx"]
    if ctx.myid == 0:
        ctx.set_shape(mumps_case["n"])
        ctx.set_centralized_assembled(mumps_case["irn"], mumps_case["jcn"], mumps_case["aval"])
        x = mumps_case["rhs"].copy()
        ctx.set_rhs(x)
    ctx.destroy()
    assert ctx.destroyed


def test_analyze(mumps_case):
    ctx = mumps_case["ctx"]
    if ctx.myid == 0:
        ctx.set_shape(mumps_case["n"])
        ctx.set_centralized_assembled(mumps_case["irn"], mumps_case["jcn"], mumps_case["aval"])
    ctx.run(job=1)
    assert ctx.id.infog[0] >= 0
    ctx.destroy()
    assert ctx.destroyed


def test_factorize(mumps_case):
    ctx = mumps_case["ctx"]
    if ctx.myid == 0:
        ctx.set_shape(mumps_case["n"])
    ctx.set_centralized_assembled(mumps_case["irn"], mumps_case["jcn"], mumps_case["aval"])
    ctx.run(job=4)
    assert ctx.id.infog[0] >= 0
    ctx.destroy()
    assert ctx.destroyed


def test_solve(mumps_case):
    ctx = mumps_case["ctx"]
    if ctx.myid == 0:
        ctx.set_shape(mumps_case["n"])
        ctx.set_centralized_assembled(mumps_case["irn"], mumps_case["jcn"], mumps_case["aval"])
    x = mumps_case["rhs"].copy()
    if ctx.myid == 0:
        ctx.set_rhs(x)
    ctx.run(job=6)
    assert ctx.id.infog[0] >= 0
    ctx.destroy()
    assert ctx.destroyed
    if ctx.myid == 0:
        assert np.allclose(x,  mumps_case["sol"])
    
    
def test_spsolve(mumps_case):
    # destroy unused context
    mumps_case["ctx"].destroy()
    # build matrix
    A = sp.sparse.coo_matrix((mumps_case["aval"], (mumps_case["irn"] - 1, mumps_case["jcn"] - 1)), 
                             shape=(mumps_case["n"], mumps_case["n"]))
    sol = mumps.spsolve(A, mumps_case["rhs"])
    if comm.rank == 0:
        assert np.allclose(sol, mumps_case["sol"])
    else:
        assert sol is None
        
def test_spsolve_sparse_rhs(mumps_case):
    # destroy unused context
    mumps_case["ctx"].destroy()
    # build matrix
    A = sp.sparse.coo_matrix((mumps_case["aval"], (mumps_case["irn"] - 1, mumps_case["jcn"] - 1)), 
                             shape=(mumps_case["n"], mumps_case["n"]))
    rhs_sparse = sp.sparse.coo_matrix(mumps_case["rhs"])
    sol = mumps.spsolve(A, rhs_sparse)
    if comm.rank == 0:
        assert np.allclose(sol, mumps_case["sol"])
    else:
        assert sol is None
        
def test_factorize(mumps_case):
    # destroy unused context
    mumps_case["ctx"].destroy()
    # factorize matrix
    A = sp.sparse.coo_matrix((mumps_case["aval"], (mumps_case["irn"] - 1, mumps_case["jcn"] - 1)), 
                             shape=(mumps_case["n"], mumps_case["n"]))
    obj = mumps.factorize(A)
    # repeat solve
    sol = obj.solve(mumps_case["rhs"])
    if comm.rank == 0:
        assert np.allclose(sol, mumps_case["sol"])
    else:
        assert sol is None
    solb = obj.solve(mumps_case["rhs"])
    if comm.rank == 0:
        assert np.allclose(solb, mumps_case["sol"])
    else:
        assert solb is None
    # multiple RHS
    rhs_multiple = np.tile(mumps_case["rhs"], (3, 1))
    # multiples reference solutions
    ref_sol_multiple = np.tile(mumps_case["sol"], (3, 1))
    # solve multiple RHS
    sol_multiple = obj.solve(rhs_multiple)
    obj.destroy()
    if comm.rank == 0:
        assert np.allclose(sol_multiple, ref_sol_multiple)
    else:
        assert sol_multiple is None
    
def test_factorize_sparse(mumps_case):
    # destroy unused context
    mumps_case["ctx"].destroy()
    # factorize matrix
    A = sp.sparse.coo_matrix((mumps_case["aval"], (mumps_case["irn"] - 1, mumps_case["jcn"] - 1)), 
                             shape=(mumps_case["n"], mumps_case["n"]))
    obj = mumps.factorize(A)
    rhs_sparse = sp.sparse.coo_matrix(mumps_case["rhs"])
    # repeat solve
    # sol = obj.solve(rhs_sparse)
    # if comm.rank == 0:
    #     assert np.allclose(sol, mumps_case["sol"])
    # else:
    #     assert sol is None
    # solb = obj.solve(rhs_sparse)
    # if comm.rank == 0:
    #     assert np.allclose(solb, mumps_case["sol"])
    # else:
    #     assert solb is None
        
    # solc = obj.solve(mumps_case["rhs"]) # come back to non sprase format
    # if comm.rank == 0:
    #     assert np.allclose(solc, mumps_case["sol"])
    # else:
    #     assert solc is None
    # multiple RHS
    rhs_multiple = np.tile(mumps_case["rhs"], (3, 1))
    rhs_multiple_sparse = sp.sparse.coo_matrix(rhs_multiple)
    # multiples reference solutions
    ref_sol_multiple = np.tile(mumps_case["sol"], (3, 1))
    # solve multiple RHS
    sol_multiple = obj.solve(rhs_multiple_sparse)
    obj.destroy()
    if comm.rank == 0:
        assert np.allclose(sol_multiple, ref_sol_multiple)
    else:
        assert sol_multiple is None


def test_factorize_det(mumps_case):
    # destroy unused context
    mumps_case["ctx"].destroy()
    # factorize matrix with determinant computation enabled (default)
    A = sp.sparse.coo_matrix((mumps_case["aval"], (mumps_case["irn"] - 1, mumps_case["jcn"] - 1)),
                             shape=(mumps_case["n"], mumps_case["n"]))
    obj = mumps.factorize(A)
    det_val = obj.det
    obj.destroy()

    if comm.rank == 0:
        det_ref = np.linalg.det(A.toarray().astype(mumps_case["dtype"]))
        assert np.allclose(det_val, det_ref)
    else:
        assert det_val is None


def test_factorize_det_disabled(mumps_case):
    # destroy unused context
    mumps_case["ctx"].destroy()
    # factorize matrix with determinant computation explicitly disabled
    A = sp.sparse.coo_matrix((mumps_case["aval"], (mumps_case["irn"] - 1, mumps_case["jcn"] - 1)),
                             shape=(mumps_case["n"], mumps_case["n"]))
    obj = mumps.factorize(A, options={"det": False})

    if comm.rank == 0:
        with pytest.warns(UserWarning, match="Determinant was not computed"):
            det_val = obj.det
        assert det_val is None
    else:
        det_val = obj.det
        assert det_val is None

    obj.destroy()
