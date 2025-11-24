import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def exact_solution(x):
    """您推導出的真值解 (設定 C2=0 -> u(0)=0)"""
    return (x / (2 * np.pi)) - (np.sin(2 * np.pi * x) / (4 * np.pi**2))

def solve_neumann_fdm(N):
    h = 1.0 / N
    x = np.linspace(0, 1, N+1)
    dim = N + 1
    A = np.zeros((dim, dim))
    b = np.zeros(dim)
    
    # 建立 Source term
    f = np.sin(2 * np.pi * x)
    
    # 1. 內部節點
    for i in range(1, N):
        A[i, i-1] = 1.0
        A[i, i]   = -2.0
        A[i, i+1] = 1.0
        b[i]      = (h**2) * f[i]
        
    # 2. 左邊界 (Ghost Point 推導結果: -2u0 + 2u1 = 0)
    A[0, 0] = -2.0
    A[0, 1] = 2.0
    b[0]    = (h**2) * f[0] # f(0)=0
    
    # 3. 右邊界 (Ghost Point 推導結果: 2u_{N-1} - 2u_N = 0)
    A[N, N-1] = 2.0
    A[N, N]   = -2.0
    b[N]      = (h**2) * f[N] # f(1)=0
    
    # 4. 求解奇異矩陣
    # 使用 Least Squares 求解
    u_raw, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
    
    # 5. 平移解 (Shift)
    # 您的真值解是 u(0)=0，所以我們將數值解整條平移，讓 u_num[0] = 0
    u_sol = u_raw - u_raw[0]
    
    return x, u_sol

# --- 驗證與收斂性測試 ---
print(f"{'N':<5} | {'h':<8} | {'Max Error':<12} | {'Ratio':<6} | {'Order':<6}")
print("-" * 55)

prev_error = None
N_values = [10, 20, 40, 80, 160]

for N in N_values:
    x, u_fdm = solve_neumann_fdm(N)
    u_true = exact_solution(x)
    
    # 計算最大誤差
    max_err = np.max(np.abs(u_fdm - u_true))
    
    ratio_str = "N/A"
    order_str = "N/A"
    
    if prev_error is not None:
        ratio = prev_error / max_err
        order = np.log2(ratio)
        ratio_str = f"{ratio:.2f}"
        order_str = f"{order:.2f}"
    
    print(f"{N:<5} | {1/N:<8.4f} | {max_err:.4e}   | {ratio_str:<6} | {order_str:<6}")
    prev_error = max_err

# --- 繪圖 (使用 N=40) ---
x_plot, u_plot = solve_neumann_fdm(40)
u_true_plot = exact_solution(x_plot)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(x_plot, u_true_plot, 'k-', label='Exact')
plt.plot(x_plot, u_plot, 'r--', label='FDM N=40')
plt.legend()
plt.title('Solution Comparison')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(x_plot, u_plot - u_true_plot, 'b-') # 有號誤差
plt.title('Error Distribution (Numeric - Exact)')
plt.grid(True)
plt.tight_layout()
plt.show()
