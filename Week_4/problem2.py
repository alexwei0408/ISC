# Fix printing for mpmath numbers and re-run the key parts quickly

import numpy as np
import mpmath as mp
import math

def f_orig(x: float) -> float:
    if x == 0.0:
        return -mp.inf
    return mp.log(x) / (1 + 25 * x * x)

def g_trans(x: float) -> float:
    if x == 0.0:
        return -1.0
    return -0.2 * mp.atan(5 * x) / x

# Trapezoid result previously computed with N=2000
N = 2000
a, b = 0.0, 1.0
x_nodes = np.linspace(a, b, N)
h = (b - a) / (N - 1)
g_vals = np.array([float(g_trans(x)) for x in x_nodes])
trap_sum = 0.5 * (g_vals[0] + g_vals[-1]) + g_vals[1:-1].sum()
I_trap = h * trap_sum

# High-precision true integral via mpmath
mp.mp.dps = 60
I_true = mp.quad(lambda t: f_orig(t), [0, 1])
abs_err = abs(float(I_trap) - float(I_true))

print(f"N (nodes)              : {N}")
print(f"h (step size)          : {h:.12f}")
print(f"Trapezoid approximation: {I_trap:.15f}")
print("High-precision (mpmath):", mp.nstr(I_true, 20))
print(f"Absolute error         : {abs_err:.3e}")
