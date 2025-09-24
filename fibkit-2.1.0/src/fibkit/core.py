import math
import operator
from dataclasses import dataclass
from typing import Any, Dict, Generator, List, Tuple, Optional
class FibonacciError(Exception): pass
@dataclass
class FibonacciConfig:
    max_safe_binet: int = 70
    sequence_limit: int = 100_000
    use_binet_for_small_n: bool = True
class FibonacciEngine:
    def __init__(self, config: Optional[FibonacciConfig] = None):
        self.config = config or FibonacciConfig()
        self._small_fib_cache = self._precompute_small_fibonacci(1000)

    @staticmethod
    def _require_int(value: Any, *, desc: str) -> int:
        if isinstance(value, bool):
            raise FibonacciError(f"{desc} must be integer, got {type(value)}")
        try:
            return operator.index(value)
        except TypeError:
            raise FibonacciError(f"{desc} must be integer, got {type(value)}") from None

    @staticmethod
    def _require_non_negative(value: Any, *, desc: str) -> int:
        if isinstance(value, bool):
            raise FibonacciError(f"{desc} must be non-negative integer, got {value}")
        try:
            result = operator.index(value)
        except TypeError:
            raise FibonacciError(f"{desc} must be non-negative integer, got {value}") from None
        if result < 0:
            raise FibonacciError(f"{desc} must be non-negative integer, got {value}")
        return result

    @staticmethod
    def _require_positive(value: Any, *, desc: str) -> int:
        if isinstance(value, bool):
            raise FibonacciError(f"{desc} must be positive integer, got {value}")
        try:
            result = operator.index(value)
        except TypeError:
            raise FibonacciError(f"{desc} must be positive integer, got {value}") from None
        if result <= 0:
            raise FibonacciError(f"{desc} must be positive integer, got {value}")
        return result
    def _precompute_small_fibonacci(self, n: int) -> List[int]:
        if n < 2: return [0,1][:n+1]
        fibs=[0,1]
        for i in range(2,n+1): fibs.append(fibs[i-1]+fibs[i-2])
        return fibs
    def _fast_doubling(self, n: int) -> Tuple[int,int]:
        if n==0: return (0,1)
        a,b=self._fast_doubling(n>>1)
        c=a*(2*b-a); d=a*a+b*b
        return (d,c+d) if (n&1) else (c,d)
    def _fast_doubling_mod(self, n:int, m:int)->Tuple[int,int]:
        if m<=0: raise FibonacciError(f"modulus must be positive, got {m}")
        if n==0: return (0%m,1%m)
        a,b=self._fast_doubling_mod(n>>1,m)
        c=(a*((2*b-a)%m))%m; d=(a*a+b*b)%m
        return (d,(c+d)%m) if (n&1) else (c,d)
    def fibonacci(self,n:int)->int:
        n=self._require_int(n, desc="Input")
        if n<0: raise FibonacciError(f"Fibonacci undefined for negative n: {n}")
        if self.config.use_binet_for_small_n and n<=self.config.max_safe_binet: return self.fibonacci_binet(n)
        if n<len(self._small_fib_cache): return self._small_fib_cache[n]
        return self._fast_doubling(n)[0]
    def lucas(self,n:int)->int:
        n=self._require_int(n, desc="Input")
        if n<0: raise FibonacciError(f"Lucas undefined for negative n: {n}")
        f_n,f_np1=self._fast_doubling(n); return 2*f_np1 - f_n
    def fibonacci_binet(self,n:int)->int:
        n=self._require_int(n, desc="Input")
        if n<0: raise FibonacciError(f"Fibonacci undefined for negative n: {n}")
        if n>self.config.max_safe_binet:
            raise FibonacciError(
                f"Binet's formula unreliable for n > {self.config.max_safe_binet}"
            )
        sqrt5=math.sqrt(5.0); phi=(1.0+sqrt5)/2.0; psi=(1.0-sqrt5)/2.0
        return int(round((phi**n-psi**n)/sqrt5))
    def fibonacci_sequence(self,limit:int)->Generator[int,None,None]:
        limit=self._require_non_negative(limit, desc="Limit")
        if limit>self.config.sequence_limit:
            raise FibonacciError(
                f"Sequence limit {self.config.sequence_limit} exceeded: {limit}"
            )
        a,b=0,1
        for _ in range(limit): yield a; a,b=b,a+b
    def generate_sequence(self,method:str="iterative",limit:int=20)->List[int]:
        limit=self._require_non_negative(limit, desc="Limit")
        if method=="iterative": return list(self.fibonacci_sequence(limit))
        elif method=="fast_doubling": return [self._fast_doubling(i)[0] for i in range(limit)]
        elif method=="binet":
            safe=min(limit,self.config.max_safe_binet+1)
            seq=[self.fibonacci_binet(i) for i in range(safe)]
            if safe<limit: seq.extend(self._fast_doubling(i)[0] for i in range(safe,limit))
            return seq
        else: raise FibonacciError(f"Unknown method '{method}'. Available: ['iterative','fast_doubling','binet']")
    def fibonacci_mod(self,n:int,m:int)->int:
        n=self._require_int(n, desc="n")
        if n<0: raise FibonacciError(f"Fibonacci undefined for negative n: {n}")
        m=self._require_positive(m, desc="modulus")
        return self._fast_doubling_mod(n,m)[0]
    def pisano_period(self,m:int)->int:
        m=self._require_positive(m, desc="modulus")
        if m==1: return 1
        prev,curr=0,1
        for p in range(1,6*m+1):
            prev,curr=curr,(prev+curr)%m
            if prev==0 and curr==1: return p
        raise FibonacciError("Pisano period search exceeded theoretical bound.")
    def analyze_fibonacci(self,n:int)->Dict[str,Any]:
        n=self._require_int(n, desc="Input")
        if n<0: raise FibonacciError(f"Analysis undefined for negative n: {n}")
        fn=self.fibonacci(n); fn1=self.fibonacci(n+1)
        golden=(fn1/fn) if n>=2 else None
        return {"n":n,"fibonacci_number":fn,"digit_count":len(str(fn)),"is_even":(fn%2==0),
                "golden_ratio_approximation":golden,
                "log10_approximation": n*math.log10((1+math.sqrt(5))/2)-math.log10(math.sqrt(5))}
def fib(n:int,*,cfg:Optional[FibonacciConfig]=None)->int: return FibonacciEngine(cfg).fibonacci(n)
def lucas(n:int,*,cfg:Optional[FibonacciConfig]=None)->int: return FibonacciEngine(cfg).lucas(n)
def fib_mod(n:int,m:int)->int: return FibonacciEngine().fibonacci_mod(n,m)
def pisano_period(m:int)->int: return FibonacciEngine().pisano_period(m)
