# Target: drive absolute error below 1e-10 using ONLY composite trapezoidal rule on the transformed integrand.
# Strategy: keep doubling the number of subintervals until |error| <= 1e-10.
# (This preserves the "composite trapezoidal rule" requirement, no Romberg/Simpson.)
#
# We'll reuse the previous definitions and recompute I_true once with high precision.

import numpy as np
import mpmath as mp
import math
import matplotlib.pyplot as plt

mp.mp.dps = 70  # higher precision for the reference integral

def f_orig(x: float):
    if x == 0.0:
        return -mp.inf
    return mp.log(x) / (1 + 25 * x * x)

def g_trans(x: float):
    if x == 0.0:
        return -1.0
    return -0.2 * mp.atan(5 * x) / x

# High-precision reference
I_true = mp.quad(lambda t: f_orig(t), [0, 1])

# Composite trapezoid on [0,1] with N nodes
def trap_integral(N: int) -> float:
    a, b = 0.0, 1.0
    x = np.linspace(a, b, N)
    h = (b - a) / (N - 1)
    gvals = np.array([float(g_trans(xi)) for xi in x])
    s = 0.5 * (gvals[0] + gvals[-1]) + gvals[1:-1].sum()
    return float(h * s)

# Search for N that achieves error <= 1e-10
tol = 1e-10
N0 = 2000  # starting from user's original request
Ns = []
errs = []

N = N0
while True:
    I_trap = trap_integral(N)
    err = abs(I_trap - float(I_true))
    Ns.append(N)
    errs.append(err)
    if err <= tol:
        break
    # double the number of subintervals ⇒ double (N-1) and add 1 for nodes
    N = 2 * (N - 1) + 1

# Report best result
print("High-precision (mpmath):", mp.nstr(I_true, 25))
print(f"Achieved tolerance {tol:g} with:")
print(f"  N (nodes)      : {N}")
print(f"  h (step size)  : {1.0/(N-1):.12f}")
print(f"  Trapezoid      : {I_trap:.15f}")
print(f"  Absolute error : {err:.3e}")

# Plot convergence of error vs N (log-log)
plt.figure()
plt.loglog(Ns, errs, marker='o')
plt.xlabel("N (number of nodes)")
plt.ylabel("Absolute error")
plt.title("Composite Trapezoid Error Convergence")
plt.grid(True, which='both')
plt.show()
