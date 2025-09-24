import random, pytest
from fibkit.core import FibonacciEngine, FibonacciConfig, FibonacciError
from fibkit.linrec import linrec2, linrec_k

def test_known_values():
    eng=FibonacciEngine()
    assert eng.fibonacci(0)==0
    assert eng.fibonacci(1)==1
    assert eng.fibonacci(2)==1
    assert eng.fibonacci(10)==55
    assert eng.fibonacci(50)==12586269025
    assert str(eng.fibonacci(100))[-10:]=="9261915075"

def test_sequences_match_and_binet_padding():
    eng=FibonacciEngine(); limit=30
    it=eng.generate_sequence("iterative",limit)
    fd=eng.generate_sequence("fast_doubling",limit)
    bn=eng.generate_sequence("binet",limit)
    assert len(it)==len(fd)==len(bn)==limit
    assert it==fd
    safe=min(limit,eng.config.max_safe_binet+1)
    assert bn[:safe]==it[:safe]

def test_lucas_identity():
    eng=FibonacciEngine()
    for n in range(0,40):
        f_n,f_np1=eng._fast_doubling(n)
        assert eng.lucas(n)==2*f_np1 - f_n

def test_modular_and_pisano():
    eng=FibonacciEngine(); rng=random.Random(7)
    for _ in range(10):
        m=rng.randint(2,200)
        pi=eng.pisano_period(m); n=rng.randint(0,2000)
        assert eng.fibonacci_mod(n,m)==eng.fibonacci_mod(n%pi,m)

def test_errors_and_guards():
    eng=FibonacciEngine(FibonacciConfig(sequence_limit=5))
    with pytest.raises(FibonacciError): eng.fibonacci(-1)
    with pytest.raises(FibonacciError): eng.fibonacci(3.14)
    with pytest.raises(FibonacciError): eng.fibonacci(True)
    with pytest.raises(FibonacciError):
        gen=eng.fibonacci_sequence(6); next(gen)
    with pytest.raises(FibonacciError): eng.fibonacci_binet(10**9)

def test_big_perf_sanity():
    eng=FibonacciEngine(); f=eng.fibonacci(10_000)
    assert len(str(f))>=2090

def test_linrec2_matches_fib_and_lucas():
    for n in range(0,50):
        assert linrec2(n,0,1,1,1)==FibonacciEngine().fibonacci(n)
    for n in range(0,50):
        assert linrec2(n,2,1,1,1)==FibonacciEngine().lucas(n)

def test_linrec_k_general():
    for n in range(0,40):
        assert linrec_k(n,[1,1],[0,1])==FibonacciEngine().fibonacci(n)
    init=[0,1,1]; coeffs=[1,1,1]
    seq=[*init]
    for _ in range(3,20):
        seq.append(seq[-1]+seq[-2]+seq[-3])
    for n in range(0,20):
        assert linrec_k(n,coeffs,init)==seq[n]
