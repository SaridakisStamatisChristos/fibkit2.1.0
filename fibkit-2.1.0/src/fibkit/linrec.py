import operator
from typing import List, Optional, Sequence


def _coerce_int(value, desc: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{desc} must be integer, got bool")
    try:
        return operator.index(value)
    except TypeError:
        raise ValueError(
            f"{desc} must be integer, got {type(value).__name__}"
        ) from None


def _coerce_non_negative_int(value, desc: str) -> int:
    result = _coerce_int(value, desc)
    if result < 0:
        raise ValueError(f"{desc} must be non-negative integer, got {result}")
    return result


def _coerce_int_sequence(values: Sequence[int], desc: str) -> List[int]:
    return [_coerce_int(v, f"{desc}[{i}]") for i, v in enumerate(values)]

def _mat2_mul(A, B):
    return (
        A[0]*B[0] + A[1]*B[2],
        A[0]*B[1] + A[1]*B[3],
        A[2]*B[0] + A[3]*B[2],
        A[2]*B[1] + A[3]*B[3],
    )

def _mat2_pow(A, n: int):
    r = (1,0,0,1)
    while n>0:
        if n&1: r=_mat2_mul(r,A)
        A=_mat2_mul(A,A); n>>=1
    return r

def linrec2(n:int, a0:int, a1:int, p:int, q:int)->int:
    n=_coerce_non_negative_int(n, "n")
    a0=_coerce_int(a0, "a0")
    a1=_coerce_int(a1, "a1")
    p=_coerce_int(p, "p")
    q=_coerce_int(q, "q")
    if n==0: return a0
    if n==1: return a1
    M=(p,q,1,0)
    Mn1=_mat2_pow(M, n-1)
    return Mn1[0]*a1 + Mn1[1]*a0

def linrec_k(n:int, coeffs:Sequence[int], init:Sequence[int])->int:
    n=_coerce_non_negative_int(n, "n")
    coeffs=list(_coerce_int_sequence(coeffs, "coeffs"))
    init=list(_coerce_int_sequence(init, "init"))
    k=len(coeffs)
    if k==0:
        raise ValueError("coeffs must not be empty")
    if len(init)!=k: raise ValueError("init must have same length as coeffs")
    if n<k: return init[n]
    # companion matrix
    M=[[0]*k for _ in range(k)]
    M[0]=list(coeffs)
    for i in range(1,k): M[i][i-1]=1
    def mul(X,Y):
        return [[sum(X[i][t]*Y[t][j] for t in range(k)) for j in range(k)] for i in range(k)]
    def mpow(A,e):
        R=[[int(i==j) for j in range(k)] for i in range(k)]
        while e>0:
            if e&1: R=mul(R,A)
            A=mul(A,A); e>>=1
        return R
    v=[init[k-1-i] for i in range(k)]
    P=mpow(M, n-(k-1))
    return sum(P[0][j]*v[j] for j in range(k))

def linrec2_array(ns: Sequence[int], a0:int, a1:int, p:int, q:int, *, numpy: Optional[object]=None):
    if numpy is None:
        try:
            import numpy as np
        except Exception:
            numpy=None
    if numpy is None:
        return [linrec2(n, a0, a1, p, q) for n in ns]
    np=numpy
    arr = np.asarray(ns, dtype=object)
    return np.array([linrec2(n, a0, a1, p, q) for n in arr], dtype=object)
