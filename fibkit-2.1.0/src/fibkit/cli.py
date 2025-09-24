import argparse, time
from .core import FibonacciEngine, FibonacciConfig, FibonacciError
from .linrec import linrec2, linrec_k

def main() -> None:
    parser = argparse.ArgumentParser(prog="fibkit", description="Fibonacci/Lucas toolkit CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_fib = sub.add_parser("fib", help="Compute F(n)")
    p_fib.add_argument("n", type=int)
    p_fib.add_argument("--binet-cutoff", type=int, default=70)

    p_luc = sub.add_parser("lucas", help="Compute L(n)")
    p_luc.add_argument("n", type=int)

    p_mod = sub.add_parser("mod", help="Compute F(n) mod m")
    p_mod.add_argument("n", type=int)
    p_mod.add_argument("m", type=int)

    p_seq = sub.add_parser("seq", help="Emit F(0..limit-1)")
    p_seq.add_argument("limit", type=int)
    p_seq.add_argument("--method", choices=["iterative", "fast_doubling", "binet"], default="iterative")

    p_pi = sub.add_parser("pisano", help="Compute Pisano period π(m)")
    p_pi.add_argument("m", type=int)

    p_lr = sub.add_parser("linrec", help="2nd-order linear recurrence a(n)=p*a(n-1)+q*a(n-2)")
    p_lr.add_argument("--n", type=int, required=True)
    p_lr.add_argument("--a0", type=int, required=True)
    p_lr.add_argument("--a1", type=int, required=True)
    p_lr.add_argument("--p", type=int, required=True)
    p_lr.add_argument("--q", type=int, required=True)

    p_lrk = sub.add_parser("linrec-k", help="k-th order linear recurrence with coeffs & init")
    p_lrk.add_argument("--n", type=int, required=True)
    p_lrk.add_argument("--coeffs", type=int, nargs="+", required=True)
    p_lrk.add_argument("--init", type=int, nargs="+", required=True)

    p_bench = sub.add_parser("bench", help="Run small benchmark table")

    args = parser.parse_args()

    try:
        if args.cmd == "fib":
            eng = FibonacciEngine(FibonacciConfig(max_safe_binet=args.binet_cutoff))
            print(eng.fibonacci(args.n))
        elif args.cmd == "lucas":
            print(FibonacciEngine().lucas(args.n))
        elif args.cmd == "mod":
            print(FibonacciEngine().fibonacci_mod(args.n, args.m))
        elif args.cmd == "seq":
            print(FibonacciEngine().generate_sequence(args.method, args.limit))
        elif args.cmd == "pisano":
            print(FibonacciEngine().pisano_period(args.m))
        elif args.cmd == "linrec":
            print(linrec2(args.n, args.a0, args.a1, args.p, args.q))
        elif args.cmd == "linrec-k":
            print(linrec_k(args.n, args.coeffs, args.init))
        elif args.cmd == "bench":
            eng = FibonacciEngine()
            cases = [10, 100, 1000, 10_000, 100_000]
            print("n\tF(n) digits\tfib(ms)")
            for n in cases:
                t0 = time.time()
                fn = eng.fibonacci(n)
                ms = (time.time()-t0)*1000
                print(f"{n}\t{len(str(fn))}\t{ms:.3f}")
    except FibonacciError as e:
        parser.error(str(e))
