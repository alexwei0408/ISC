import math
import numpy as np
from scipy.interpolate import BarycentricInterpolator

# ---- target function ----
def f(x):
    return 1.0 / (1.0 + 25.0 * x * x)

# ---- Chebyshev–Lobatto nodes on [-1,1] ----
# m = number of nodes (includes endpoints), degree = m-1
def cheb_lobatto_nodes(m: int) -> np.ndarray:
    if m < 2:
        raise ValueError("m (number of nodes) must be >= 2")
    k = np.arange(m)
    x = np.cos(np.pi * k / (m - 1))        # from 1 to -1
    return np.sort(x)                      # ascending: [-1,...,1]

# ---- max error on dense grid ----
def max_error(interp, a=-1.0, b=1.0, samples=20001) -> float:
    xs = np.linspace(a, b, samples)
    err = np.abs(f(xs) - interp(xs))
    return float(np.max(err))

# ---- search minimal m (nodes) to meet tol ----
def find_min_nodes(tol=1e-10, m_start=8, m_max=2000, samples=20001, verbose=True):
    # exponential ramp-up to bracket, then binary search for minimal m
    def err_for(m):
        x = cheb_lobatto_nodes(m)
        y = f(x)
        itp = BarycentricInterpolator(x, y)
        return max_error(itp, -1.0, 1.0, samples)

    m = m_start
    e = err_for(m)
    if verbose:
        print(f"m={m:4d} (deg={m-1:4d})  max_err={e:.3e}")
    if e < tol:
        return m, e

    # grow until error < tol or reach cap
    prev_m, prev_e = m, e
    while m < m_max:
        m = min(2*m, m_max)
        e = err_for(m)
        if verbose:
            print(f"m={m:4d} (deg={m-1:4d})  max_err={e:.3e}")
        if e < tol:
            lo, hi = prev_m + 1, m
            # binary search minimal m in [lo, hi]
            best_m, best_e = m, e
            while lo <= hi:
                mid = (lo + hi) // 2
                emid = err_for(mid)
                if verbose and (hi - lo <= 4):
                    print(f"  check m={mid:4d} -> {emid:.3e}")
                if emid < tol:
                    best_m, best_e = mid, emid
                    hi = mid - 1
                else:
                    lo = mid + 1
            return best_m, best_e
        prev_m, prev_e = m, e

    return None, None  # not found up to m_max

def main():
    tol = 1e-10
    samples = 20001   # dense enough to estimate max error
    m_start = 8
    m_max = 4000

    print("=== Chebyshev (Lobatto) polynomial interpolation ===")
    print("Function: f(x) = 1 / (1 + 25 x^2) on [-1,1]")
    print(f"Target tolerance      : {tol:.1e}")
    print(f"Verification samples  : {samples}\n")

    m, err = find_min_nodes(tol, m_start, m_max, samples, verbose=True)

    if m is None:
        print("\nNo solution found up to m_max; increase the cap.")
        return

    print("\n--- RESULT ---")
    print(f"Minimal number of nodes m : {m}")
    print(f"Polynomial degree         : {m-1}")
    print(f"Measured max error        : {err:.3e}")

if __name__ == "__main__":
    main()
