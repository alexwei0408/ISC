# spline_verify.py
# f(x) = 1 / (1 + 25x^2), interval [-1,1]
# 1) 用公式計算最小 N，對 tol=1e-10, 1e-14
# 2) 用 scipy 做 natural / clamped cubic spline，驗證實際誤差

import numpy as np
import sympy as sp
from scipy.interpolate import CubicSpline

# --- Step 1: 最大四階導數 ---
def max_abs_fourth_derivative():
    x = sp.symbols('x', real=True)
    f = 1 / (1 + 25*x**2)
    f4 = sp.simplify(sp.diff(f, x, 4))
    g = sp.simplify(f4**2)
    dg = sp.diff(g, x)
    num, den = sp.together(dg).as_numer_denom()
    roots = sp.nroots(sp.Poly(num, x))

    cand = {-1.0, 0.0, 1.0}
    for r in roots:
        if abs(sp.im(r)) < 1e-12:
            val = float(sp.re(r))
            if -1.0 <= val <= 1.0:
                cand.add(val)

    f4_np = sp.lambdify(x, f4, "numpy")
    M = max(abs(float(f4_np(c))) for c in cand)
    return float(M), f4

# --- Step 2: 公式計算最小 N ---
def minimal_N_for_tol(M, tol):
    const = (5/384) * M
    return int(np.ceil(2 * ((const / tol) ** 0.25)))

# --- Step 3: 驗證誤差 ---
def verify_spline(N, bc_type="natural"):
    f = lambda x: 1 / (1 + 25*x**2)
    x_nodes = np.linspace(-1, 1, N+1)
    y_nodes = f(x_nodes)

    if bc_type == "natural":
        spline = CubicSpline(x_nodes, y_nodes, bc_type="natural")
    elif bc_type == "clamped":
        # f'(x) = -50x / (1+25x^2)^2
        fprime = lambda x: -50*x / (1 + 25*x**2)**2
        spline = CubicSpline(x_nodes, y_nodes,
                             bc_type=((1, fprime(-1)), (1, fprime(1))))
    else:
        raise ValueError("bc_type must be 'natural' or 'clamped'")

    # dense grid for error check
    x_dense = np.linspace(-1, 1, 5001)
    err = np.max(np.abs(f(x_dense) - spline(x_dense)))
    return err

def main():
    M, f4 = max_abs_fourth_derivative()
    print("f''''(x) =", f4)
    print(f"max |f''''(x)| = {M:.6f}\n")

    for tol in [1e-10, 1e-14]:
        N = minimal_N_for_tol(M, tol)
        h = 2 / N
        bound_val = (5/384) * (h**4) * M
        print(f"Tolerance {tol:.0e}:")
        print(f"  Minimal N = {N}")
        print(f"  Bound value = {bound_val:.3e}")

        # 驗證 natural 與 clamped 誤差
        err_nat = verify_spline(N, "natural")
        err_cla = verify_spline(N, "clamped")
        print(f"  Actual max error (natural) = {err_nat:.3e}")
        print(f"  Actual max error (clamped) = {err_cla:.3e}\n")

if __name__ == "__main__":
    main()
