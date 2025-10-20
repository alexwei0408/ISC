# logistic_fe_h_scan_fixed.py
# Scan h = 0.1, 0.2, ..., 2.1 for Forward Euler on y' = y(1-y)
# Show invariance & convergence. Expect:
#   - Full invariance for ALL u0 in (0,1): holds for 0 < h <= 1
#   - Local stability near y=1: holds for 0 < h < 2
#   - Example: h=2.1 overshoots/exits.

import numpy as np
import matplotlib.pyplot as plt

def fe_logistic(h, u0=0.2, steps=200):
    """Forward Euler trajectory for y' = y(1-y). Returns u[0..steps]."""
    u = np.empty(steps+1, dtype=float)
    u[0] = u0
    for n in range(steps):
        u[n+1] = u[n] + h*u[n]*(1.0 - u[n])
    return u

def invariance_single(u, tol=1e-12):
    """Check (0,1) invariance on this single trajectory (allow tiny FP wiggle)."""
    return (u.min() > -tol) and (u.max() < 1.0 + tol)

def invariance_all_u0(h, steps=1, grid=2001, tol=1e-12):
    """
    Check full-interval invariance: for a dense grid of u0 in (0,1),
    after 'steps' FE steps, result stays in (0,1).
    Using steps=1 already catches overshoot for h>1.
    """
    u0s = np.linspace(1e-9, 1.0-1e-9, grid)
    u = u0s.copy()
    for _ in range(steps):
        u = u + h*u*(1.0 - u)
    return (u.min() > -tol) and (u.max() < 1.0 + tol)

def converges_to_one(u, atol=1e-3, tail=50):
    """Check if the last 'tail' values are all within atol of 1."""
    tail = min(tail, len(u))
    return np.all(np.abs(u[-tail:] - 1.0) < atol)

def main():
    u0 = 0.2
    steps = 400  # 稍微多一些步，避免「收斂很慢」被誤判
    print(f"Forward Euler on y'=y(1-y), u0={u0}, steps={steps}\n")

    hs = [round(0.1*k, 1) for k in range(1, 22)]  # 0.1 ... 2.1

    print(f"{'h':>4} | {'inv(single)':>12} | {'inv(all u0)':>11} | {'converges?':>11} | final u")
    print("-"*64)
    for h in hs:
        traj = fe_logistic(h, u0=u0, steps=steps)
        inv_single = invariance_single(traj, tol=1e-12)
        inv_all    = invariance_all_u0(h, steps=1, grid=4001, tol=1e-12)  # 一步就能抓到 h>1 的 overshoot
        conv       = converges_to_one(traj, atol=1e-3, tail=50)
        print(f"{h:>4} | {str(inv_single):>12} | {str(inv_all):>11} | {str(conv):>11} | {traj[-1]:.6f}")

    print("\nTheory summary:")
    print("  - Full invariance for ALL u0 in (0,1):  0 < h <= 1")
    print("  - Local stability near y=1:            0 < h < 2")
    print("  - Expect h=2.1 to overshoot/exit. For 1 < h < 2, some u0 may overshoot.\n")

    # Plot illustrative trajectories
    demo_hs = [0.1, 1.0, 1.9, 2.1]
    plt.figure()
    for h in demo_hs:
        u = fe_logistic(h, u0=u0, steps=steps)
        plt.plot(range(steps+1), u, marker='.', linewidth=1, label=f"h={h}")
    plt.axhline(1.0, color='k', linestyle='--', linewidth=1)
    plt.ylim(-0.5, 1.6)
    plt.xlabel("iteration n")
    plt.ylabel("u_n")
    plt.title("Forward Euler on logistic: trajectories")
    plt.legend()
    plt.grid(True, ls=":")
    plt.tight_layout()
    plt.savefig("logistic_FE_trajectories_fixed.png", dpi=150)
    print("Saved figure: logistic_FE_trajectories_fixed.png")
    # 參考線 y=1
    plt.axhline(1.0, linestyle='--', linewidth=1)

    plt.xlabel("iteration n")
    plt.ylabel("u_n")
    plt.title("Logistic ODE with Forward Euler: h=0.5, 1.0 (no overshoot) vs h=2.0 (overshoot)")
    plt.legend()
    plt.grid(True, linestyle=':')
    plt.tight_layout()
    plt.savefig("logistic_FE_h05_h10_h20.png", dpi=150)
    print("Saved: logistic_FE_h05_h10_h20.png")

if __name__ == "__main__":
    main()
