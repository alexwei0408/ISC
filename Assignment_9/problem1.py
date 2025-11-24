import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def exact_solution(x):
    """計算解析解 (Exact Solution)"""
    u = np.zeros_like(x)
    for i, xi in enumerate(x):
        if xi <= 0.4:
            u[i] = -0.1 * xi
        elif 0.4 < xi <= 0.6:
            u[i] = 0.08 - 0.5 * xi + 0.5 * xi**2
        else:
            u[i] = -0.1 * (1 - xi)
    return u

def solve_fdm_standard(N):
    """標準 FDM 求解 (不含邊界修正)"""
    h = 1.0 / N
    x = np.linspace(0, 1, N+1)
    dim = N - 1
    A = np.zeros((dim, dim))
    b = np.zeros(dim)
    
    # 建立矩陣
    for i in range(dim):
        A[i, i] = -2.0
        if i > 0:     A[i, i-1] = 1.0
        if i < dim-1: A[i, i+1] = 1.0
        
        # 建立 RHS (標準採樣: f(x)=1 if 0.4<=x<=0.6)
        xi = x[i+1]
        # 使用極小值避免浮點數誤差
        if 0.4 - 1e-9 <= xi <= 0.6 + 1e-9:
            f_val = 1.0
        else:
            f_val = 0.0
        b[i] = (h**2) * f_val
        
    u_inner = np.linalg.solve(A, b)
    u_sol = np.zeros(N+1)
    u_sol[1:N] = u_inner
    return x, u_sol

# --- 執行收斂性測試 ---
N_values = [10, 20, 40, 80, 160, 320]
errors = []
ratios = []

print(f"{'N':<5} | {'h':<8} | {'Max Error':<12} | {'Ratio (Err_old/Err_new)':<25}")
print("-" * 60)

prev_error = None

# 用來儲存最後一次 (N=320) 的數據以供繪圖使用
final_x = None
final_u_num = None
final_u_true = None

for N in N_values:
    h = 1.0 / N
    x, u_num = solve_fdm_standard(N)
    u_true = exact_solution(x)
    
    # 儲存最後一組數據 (N=320)
    if N == N_values[-1]:
        final_x = x
        final_u_num = u_num
        final_u_true = u_true
    
    # 計算最大誤差 (L_inf norm)
    max_err = np.max(np.abs(u_num - u_true))
    errors.append(max_err)
    
    # 計算收斂比率 (Ratio)
    ratio_str = "N/A"
    if prev_error is not None:
        ratio = prev_error / max_err
        ratios.append(ratio)
        ratio_str = f"{ratio:.4f}"
    else:
        ratios.append(np.nan)
        
    print(f"{N:<5} | {h:<8.4f} | {max_err:.4e}   | {ratio_str}")
    prev_error = max_err





# --- 圖表 2: N=320 的解與誤差分佈 ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# 子圖 1: 解的對比
ax1.plot(final_x, final_u_true, 'k-', linewidth=3, alpha=0.5, label='Exact Solution')
ax1.plot(final_x, final_u_num, 'r--', linewidth=1.5, label=f'FDM (N={N_values[-1]})')
ax1.set_title(f'Exact vs FDM (N={N_values[-1]})')
ax1.set_xlabel('x')
ax1.set_ylabel('u(x)')
ax1.legend()
ax1.grid(True)

# 子圖 2: 誤差分佈
error_dist = np.abs(final_u_true - final_u_num)
max_err_val = np.max(error_dist)


ax2.plot(final_x, error_dist, 'b-', linewidth=1.5)
ax2.set_title(f'Absolute Error Distribution')
ax2.set_xlabel('x')
ax2.set_ylabel('|Exact - Numerical|')
ax2.grid(True)

# 標示不連續點的位置
ax2.axvline(0.4, color='gray', linestyle=':', alpha=0.6)
ax2.axvline(0.6, color='gray', linestyle=':', alpha=0.6)

plt.tight_layout()
plt.show()
