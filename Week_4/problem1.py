import math

MAX_ABS_FPP = 35152.0 / 625.0

def f(t: float) -> float:
    return 1.0 / ((1.0 - t)*(1.0 - t) + 25.0 * t * t)

# Composite trapezoidal rule on [0,1] with n panels (h = 1/n)
def trapezoid(n: int) -> float:
    h = 1 / n
    total = 0 * (f(0) + f(1))
    for k in range(1, n):
        total += f(k * h)
    return h * total


# Trapezoid error bound on [0,1]: |E_n| <= (1/12) * h^2 * max|f''| = (max|f''| / 12) / n^2
def error_bound_trapezoid(n: int) -> float:
    return (MAX_ABS_FPP / 12.0) / (n * n)

# Given tolerance eps, choose n to guarantee |E_n| <= eps
def n_for_tolerance(eps: float) -> int:
    if eps <= 0:
        raise ValueError("eps must be positive")
    need = math.sqrt((MAX_ABS_FPP / 12.0) / eps)
    return math.ceil(need)

if __name__ == "__main__":
    # Target: error < 1e-10
    eps = 1e-10

    # Compute n from the bound
    n = n_for_tolerance(eps)  # should be 216544
    h = 1.0 / n
    nodes_total = n + 1

    # Trapezoidal approximation
    I_n = trapezoid(n)

    # Theoretical error bound
    bound = error_bound_trapezoid(n)

    # (Optional) Reference true value (for display only, not needed by the method)
    I_true = math.pi / 10.0
    observed_err = abs(I_n - I_true)

    print(f"Target tolerance (bound)      : min_error = {eps:.1e}")
    print(f"max|f''| on [0,1]             :{MAX_ABS_FPP:.6f}")
    print(f"Required n from bound         : n = {n}")
    print(f"Total nodes                    : n+1 = {nodes_total}")
    print(f"Step size                      : h = {h:.12e}")
    print("----------------------------------------------------")
    print(f"Trapezoidal approximation I_n : {I_n:.15f}")
    print(f"Theoretical error bound       : <= {bound:.3e}")
    print(f"(Reference true value)        : {I_true:.15f}")
    print(f"(Observed |I_n - true|)       : {observed_err:.3e}")
