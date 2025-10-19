# find_h_range_logistic_fe.py
# Find step sizes h for which Forward Euler on y' = y(1-y), y in (0,1)
# preserves qualitative correctness: 0<u_{n+1}<1 for all 0<u_n<1.

import numpy as np

def forward_euler_map(u, h):
    return u + h*u*(1 - u)

def is_qualitatively_correct(h, u_min=1e-6, u_max=1-1e-6, num_u=20001):
    """
    Check if for this h, FE maps (0,1) -> (0,1): i.e., 0 < u + h*u*(1-u) < 1
    for all u in (0,1). Uses a dense grid to approximate "for all".
    """
    us = np.linspace(u_min, u_max, num_u)
    unext = forward_euler_map(us, h)
    return np.all(unext > 0.0) and np.all(unext < 1.0)

def scan_h_range(h_min=1e-4, h_max=3.0, num_h=6000, **kwargs):
    hs = np.linspace(h_min, h_max, num_h)
    ok = np.array([is_qualitatively_correct(h, **kwargs) for h in hs])
    # collect contiguous intervals where ok==True
    intervals = []
    start = None
    for i, flag in enumerate(ok):
        if flag and start is None:
            start = i
        if (not flag or i == len(ok)-1) and start is not None:
            end = i if not flag else i  # inclusive index for last True
            intervals.append((hs[start], hs[end]))
            start = None
    return hs, ok, intervals

if __name__ == "__main__":
    # Dense checks in u to be strict; adjust if you want faster runs
    hs, ok, intervals = scan_h_range(
        h_min=1e-4, h_max=3.0, num_h=6000,
        u_min=1e-8, u_max=1-1e-8, num_u=20001
    )

    print("Theoretical invariant & stability condition for FE on logistic:  0 < h < 2")
    print("\nNumerically verified admissible h intervals (approx.):")
    for (a, b) in intervals:
        print(f"  h in ({a:.4f}, {b:.4f})")

    # Optional: show a quick sanity probe near the boundary
    probes = [0.5, 1.5, 1.9, 2.0, 2.1]
    print("\nSanity checks (map (0,1)->(0,1) holds?):")
    for h in probes:
        print(f"  h={h:>4}: {is_qualitatively_correct(h)}")
