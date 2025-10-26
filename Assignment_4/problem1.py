# Convergence study for ∫_0^∞ 1/(1+25x^2) dx using the substitution x=t/(1-t)
# and composite trapezoidal rule on t∈[0,1]. We produce a log-log plot of
# absolute error vs. step size h, and overlay an O(h^2) reference line.

import math
import numpy as np
import matplotlib.pyplot as plt

# True value
true_val = math.pi / 10.0

# Transformed integrand on [0,1]:
# x = t/(1-t), dx = dt/(1-t)^2, f(x)=1/(1+25x^2)
# => integrand(t) = 1 / ( (1-t)^2 + 25 t^2 )
def f_t(t: np.ndarray) -> np.ndarray:
    return 1.0 / ((1.0 - t)**2 + 25.0 * t**2)

def trap_integral_on_unit(N: int) -> float:
    h = 1.0 / (N - 1)
    t = np.linspace(0.0, 1.0, N)
    vals = f_t(t)
    s = 0.5 * (vals[0] + vals[-1]) + vals[1:-1].sum()
    return h * s

# Build N sequence by doubling subinterval count: N -> 2*(N-1)+1
Ns = []
hs = []
errs = []
approxs = []

N = 2000  # starting nodes
tol = 1e-12  # compute a bit beyond 1e-10 to show slope clearly
while True:
    approx = trap_integral_on_unit(N)
    err = abs(approx - true_val)
    h = 1.0 / (N - 1)
    Ns.append(N); hs.append(h); errs.append(err); approxs.append(approx)
    if err <= tol or N > 200000:
        break
    N = 2 * (N - 1) + 1

# Build O(h^2) reference line passing through the first point
C = errs[0] / (hs[0]**2)
ref = [C * (h**2) for h in hs]

# Plot: error vs h (log-log), with O(h^2) reference
plt.figure()
plt.loglog(hs, errs, marker='o', label='Trapezoidal error')
plt.loglog(hs, ref, linestyle='--', label='$\mathcal{O}(h^2)$ reference')
plt.gca().invert_xaxis()  # smaller h to the right
plt.xlabel('Step size $h=1/(N-1)$')
plt.ylabel('Absolute error')
plt.title('Convergence of Composite Trapezoidal Rule (x = t/(1-t))')
plt.legend()
plt.grid(True, which='both')
plt.show()

# Also print the table
print(f"{'N(nodes)':>10}  {'h':>14}  {'Approximation':>20}  {'Abs. Error':>12}")
for N, h, a, e in zip(Ns, hs, approxs, errs):
    print(f"{N:10d}  {h:14.12f}  {a:20.15f}  {e:12.3e}")
