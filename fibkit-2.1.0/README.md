# fibkit 2.1.0

[![CI](https://github.com/yourname/fibkit/actions/workflows/ci.yml/badge.svg)](https://github.com/yourname/fibkit/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](../LICENSE)

Engineering-grade Fibonacci and Lucas toolkit for Python. **fibkit** combines mathematically sound implementations with production-friendly ergonomics so you can explore integer sequences, modular arithmetic, and general linear recurrences from a single package.

## Key features

- ⚡ **Fast integer Fibonacci** via the fast-doubling algorithm with memoised small values for common inputs.
- 🌀 **Lucas numbers** implemented through the same high-performance core.
- 🧮 **Binet's formula** support with configurable safety guards for floating-point accuracy.
- ♻️ **Sequence generation** utilities that emit Fibonacci prefixes using iterative, fast-doubling, or Binet strategies while respecting configurable limits.
- ♾️ **Modular arithmetic** helpers, including `fib_mod` and Pisano period computation.
- 🧱 **General linear recurrences** (2nd-order closed form and arbitrary order companion-matrix implementations).
- 🔧 **Configurable runtime** via `FibonacciConfig` to control Binet cut-offs and sequence limits.
- 🧰 **Command-line interface** (`fibkit`) that exposes the core functionality without writing any Python code.

## Installation

fibkit targets Python **3.9+** and has no required dependencies.

```bash
# From PyPI (recommended)
pip install fibkit

# With the optional NumPy-backed helpers
pip install 'fibkit[numpy]'

# From a cloned source tree (editable install for development)
pip install -e .
```

The optional `numpy` extra enables vectorised helpers such as `linrec2_array`.

## Quick start (Python API)

```python
from fibkit import (
    FibonacciEngine,
    FibonacciConfig,
    fib,
    lucas,
    fib_mod,
    pisano_period,
)

# Convenience helpers
print(f"F(100) = {fib(100)}")
print(f"L(10) = {lucas(10)}")
print(f"F(1_000) mod 97 = {fib_mod(1_000, 97)}")
print(f"Pisano period π(12) = {pisano_period(12)}")

# Full engine with custom configuration
config = FibonacciConfig(max_safe_binet=60, sequence_limit=10_000)
engine = FibonacciEngine(config)

# Sequence utilities
print(engine.generate_sequence(limit=10))
print(engine.generate_sequence(method="fast_doubling", limit=10))

# Inspect metadata about a Fibonacci number
summary = engine.analyze_fibonacci(250)
print(summary["digit_count"], summary["golden_ratio_approximation"])
```

### Working with sequences

- `FibonacciEngine.fibonacci_sequence(limit)` yields a generator of the first `limit` Fibonacci numbers.
- `FibonacciEngine.generate_sequence(method, limit)` returns a list with selectable strategies:
  - `iterative` – simple addition loop.
  - `fast_doubling` – reuses the fast-doubling core for every index.
  - `binet` – uses Binet's formula up to the configured safe range, then falls back to fast-doubling.
- Guardrails prevent accidentally materialising extremely large sequences; customise `FibonacciConfig.sequence_limit` if you need more.

### Modular arithmetic and Pisano periods

Use `FibonacciEngine.fibonacci_mod(n, modulus)` for exact modular values and `FibonacciEngine.pisano_period(modulus)` to compute π(m) with the canonical 6m upper bound safeguard.

## Command-line interface

The `fibkit` console script mirrors the Python API.

```bash
# Fibonacci and Lucas numbers
fibkit fib 100
fibkit lucas 20

# Modular arithmetic and Pisano period
fibkit mod 1000 97
fibkit pisano 12

# Sequence generation
fibkit seq 15 --method fast_doubling
fibkit seq 20 --method binet

# Linear recurrences
fibkit linrec --n 10 --a0 0 --a1 1 --p 1 --q 1
fibkit linrec-k --n 10 --coeffs 1 1 1 --init 0 1 1

# Benchmark sampling
fibkit bench
```

All commands provide helpful validation errors using `FibonacciError` when inputs are invalid (negative indices, unsafe Binet cut-offs, etc.).

## Linear recurrence utilities

Beyond Fibonacci numbers, fibkit ships helper functions for broader recurrences:

- `linrec2(n, a0, a1, p, q)` computes `a(n)` for the 2nd-order recurrence `a(n) = p·a(n-1) + q·a(n-2)` using matrix exponentiation.
- `linrec_k(n, coeffs, init)` evaluates k-th order recurrences from arbitrary coefficient vectors and initial seeds.
- `linrec2_array(ns, ...)` optionally leverages NumPy to bulk-evaluate a set of indices.

These helpers share the same rigorous type validation as the Fibonacci utilities.

## Project layout

```
fibkit2.1.0/
├── README.md               # This document
├── LICENSE                 # Apache 2.0 license
├── fibkit-2.1.0/
│   ├── README.md           # Package README used by PyPI
│   ├── CHANGELOG.md        # Release highlights
│   ├── pyproject.toml      # Project metadata & build configuration
│   ├── src/fibkit/         # Library sources (core engine, CLI, recurrences)
│   └── tests/              # pytest suite covering API and CLI
└── ...
```

## Development

1. Clone the repository and create a virtual environment:
   ```bash
   git clone https://github.com/yourname/fibkit.git
   cd fibkit2.1.0/fibkit-2.1.0
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install the project in editable mode with optional extras:
   ```bash
   pip install -e '.[numpy]'
   ```
3. Run the automated test suite:
   ```bash
   pytest
   ```

The test suite exercises the numerical guards, CLI entry points, and recurrence helpers to ensure regressions are caught early.

## Changelog

See [`fibkit-2.1.0/CHANGELOG.md`](fibkit-2.1.0/CHANGELOG.md) for release notes and upgrade guidance.

## License

fibkit is licensed under the [Apache License, Version 2.0](LICENSE).

## Contributing

Contributions are welcome! Please open an issue or pull request with details about the improvement or bug fix, and include tests wherever possible.
