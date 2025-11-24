import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def exact_solution(t):
    """您推導出的真值解"""
    # u(t) = 1 - e^t + ( (1 + e^-1)/2 ) * t * e^t
    c2 = (1 + np.exp(-1)) / 2
    return 1 - np.exp(t) + c2 * t * np.exp(t)

def solve_bvp_fdm(N):
    h = 1.0 / N
    t = np.linspace(0, 1, N+1)
    
    # 我們求解 u[1] 到 u[N]，共 N 個未知數 (u[0]已知為0)
    dim = N
    A = np.zeros((dim, dim))
    b = np.zeros(dim)
    
    # 係數定義
    coeff_m1 = 1 + h      # u_{i-1} 的係數
    coeff_0  = h**2 - 2   # u_i     的係數
    coeff_p1 = 1 - h      # u_{i+1} 的係數
    
    for i in range(dim):
        # 矩陣索引 i 對應到真實網格點 index = i + 1
        # 例如矩陣第 0 列代表計算 u_1 的方程式
        
        # 主對角線
        A[i, i] = coeff_0
        
        # 下對角線 (涉及 u_{i-1})
        if i > 0:
            A[i, i-1] = coeff_m1
            
        # 上對角線 (涉及 u_{i+1})
        if i < dim - 1:
            A[i, i+1] = coeff_p1
            
        # RHS
        b[i] = h**2

    # --- 修正邊界條件 ---
    
    # 1. 左邊界 (計算 u_1 時): 
    # 方程式為: (1+h)u_0 + ... = h^2
    # 因為 u_0 = 0，該項消失，不用修改 b[0]
    
    # 2. 右邊界 (計算 u_N 時，即矩陣最後一列 index = dim-1):
    # 使用推導出的鬼點公式: 2*u_{N-1} + (h^2-2)u_N = h^2 - 2h(1-h)
    
    # 修改 u_{N-1} 的係數 (變為 2)
    A[dim-1, dim-2] = 2.0
    # 修改 RHS
    b[dim-1] = h**2 - 2 * h * (1 - h)
    
    # 求解
    u_inner = np.linalg.solve(A, b)
    
    # 組合完整解 (補回 u_0)
    u_full = np.zeros(N+1)
    u_full[0] = 0
    u_full[1:] = u_inner
    
    return t, u_full

# --- 收斂性測試與結果輸出 ---

N_values = [10, 20, 40, 80, 160]
print(f"{'N':<5} | {'h':<8} | {'Max Error':<12} | {'Ratio':<6}")
print("-" * 55)

prev_error = None
for N in N_values:
    t, u_fdm = solve_bvp_fdm(N)
    u_true = exact_solution(t)
    
    # 計算最大誤差 (L_inf norm)
    max_err = np.max(np.abs(u_fdm - u_true))
    
    ratio_str = "N/A"
    
    if prev_error is not None:
        ratio = prev_error / max_err
        order = np.log2(ratio) # log2(Ratio) 應該接近 2
        ratio_str = f"{ratio:.2f}"
    
    print(f"{N:<5} | {1/N:<8.4f} | {max_err:.4e}   | {ratio_str:<6}")
    prev_error = max_err

# --- 繪圖 ---
plt.figure(figsize=(10, 5))
t_plot, u_plot = solve_bvp_fdm(40) # 畫 N=40 的圖
u_true_plot = exact_solution(t_plot)

plt.subplot(1, 2, 1)
plt.plot(t_plot, u_true_plot, 'k-', label='Exact Solution')
plt.plot(t_plot, u_plot, 'r--', label='FDM (N=40)')
plt.legend()
plt.title('Solution Comparison')
plt.xlabel('t')
plt.ylabel('u(t)')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(t_plot, np.abs(u_plot - u_true_plot), 'b-o')
plt.title('Error Distribution (N=40)')
plt.xlabel('t')
plt.ylabel('Abs Error')
plt.grid(True)

plt.tight_layout()
plt.show()
