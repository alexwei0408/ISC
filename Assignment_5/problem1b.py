# be_logistic_demo.py
# Backward Euler for y' = -5y, y(0) = 1 on [0,10]
# - For h in {0.4, 0.41, 0.1}, print EVERY iteration: (step, t, y_BE, y_true, |error|)
# - Save per-step CSVs
# - Plot iteration error vs t (log-log) for these h
# - Verify O(h) using h={0.1, 0.05, 0.025, 0.0125}

import math
import numpy as np
import matplotlib.pyplot as plt
import csv
from pathlib import Path

T_END = 10.0

# True solution y(t)= e^{-5t}
def y_true(t: float) -> float:
    return math.exp(-5.0 * t)

# Backward Euler trace
def backward_euler_trace(h: float, t_end: float = T_END):
    t = 0.0
    y = 1.0
    ts  = [t]
    ys  = [y]
    err = [abs(y - y_true(t))]
    factor = 1.0/(1.0 + 5.0*h)   # for BE: y_{n+1} = y_n/(1 + 5h)
    while t < t_end - 1e-15:
        y = y * factor
        t = t + h
        ts.append(t)
        ys.append(y)
        err.append(abs(y - y_true(t)))
    return np.array(ts), np.array(ys), np.array(err)

# Save CSV
def save_csv(filename: str, ts, ys, errs):
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["step", "t", "y_BE", "y_true", "abs_error"])
        for k, (t, y, e) in enumerate(zip(ts, ys, errs)):
            w.writerow([k, t, y, y_true(t), e])

def max_error_over_grid(h: float, t_end: float = T_END) -> float:
    ts, ys, errs = backward_euler_trace(h, t_end)
    return float(np.max(errs))

def main():
    # ========= Part 1: 三個步長，逐步印出數值解 =========
    H_LIST = [0.4, 0.41, 0.1]
    for h in H_LIST:
        ts, ys, errs = backward_euler_trace(h, T_END)
        print(f"\n=== Backward Euler with h = {h} ===")
        print(f"{'step':>4} | {'t':>8} | {'y_BE':>14} | {'y_true':>14} | {'|error|':>14}")
        print("-" * 64)
        for k, (t, y, e) in enumerate(zip(ts, ys, errs)):
            print(f"{k:4d} | {t:8.4f} | {y:14.8f} | {y_true(t):14.8e} | {e:14.8f}")

        print(f"steps = {len(ts)-1}, max|error| = {np.max(errs):.6e}, "
              f"final |e| at t={ts[-1]:.2f} = {errs[-1]:.6e}")

        save_csv(f"out_BE/be_vs_true_h{str(h).replace('.','_')}.csv", ts, ys, errs)

    # ========= Part 2: Iteration error vs t (log-log) =========
    plt.figure()
    for h in H_LIST:
        ts, ys, errs = backward_euler_trace(h, T_END)
        mask = ts > 0
        plt.loglog(ts[mask], errs[mask], marker='o', label=f"h={h}")
    plt.xlabel("t")
    plt.ylabel("Absolute error |y_BE - e^{-5t}|")
    plt.title("Iteration error (log-log) for Backward Euler (h=0.4, 0.41, 0.1)")
    plt.legend()
    plt.grid(True, which="both", ls=":")
    plt.tight_layout()
    Path("out_BE").mkdir(exist_ok=True)
    plt.savefig("out_BE/iteration_error_BE.png", dpi=150)

    # ========= Part 3: O(h) 收斂驗證 (從 h=0.1 開始) =========
    h_conv = [0.1, 0.05, 0.025, 0.0125]
    E = [max_error_over_grid(h) for h in h_conv]
    print("\nConvergence table (Backward Euler):")
    print("      h        max_error")
    for h, e in zip(h_conv, E):
        print(f"  {h:8.5f}   {e:.6e}")

    for i in range(1, len(h_conv)):
        p = math.log(E[i-1]/E[i], 2)
        print(f"  order from h={h_conv[i-1]} -> {h_conv[i]}:  p ≈ {p:.3f}")

    plt.figure()
    plt.loglog(h_conv, E, marker='o', label="Max error over [0,10]")
    c_ref = E[0] / h_conv[0]
    plt.loglog(h_conv, [c_ref*h for h in h_conv], '--', label="O(h) reference")
    plt.gca().invert_xaxis()
    plt.xlabel("h")
    plt.ylabel("Max error")
    plt.title("Backward Euler global error ~ O(h)")
    plt.legend()
    plt.grid(True, which="both", ls=":")
    plt.tight_layout()
    plt.savefig("out_BE/convergence_Oh_BE.png", dpi=150)

    print("\nSaved files in ./out_BE/")
    print(" - be_vs_true_h*.csv")
    print(" - iteration_error_BE.png")
    print(" - convergence_Oh_BE.png")

if __name__ == "__main__":
    main()
