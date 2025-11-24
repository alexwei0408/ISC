import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def exact_solution(x):
    # 修正後公式: 分母為相減
    numer = np.exp(-x) - np.exp(-100 * x)
    denom = np.exp(-1) - np.exp(-100)
    return numer / denom

def solve_sp_fdm(N, epsilon=0.01):
    h = 1.0 / N
    x = np.linspace(0, 1, N+1)
    
    # 建立矩陣系統 A u = b
    # eq: epsilon*u'' + (1+epsilon)*u' + u = 0
    dim = N - 1
    A = np.zeros((dim, dim))
    b = np.zeros(dim)
    
    # 係數 (使用中央差分 Central Difference)
    # u_{i-1}: epsilon/h^2 - (1+epsilon)/(2h)
    # u_i    : -2*epsilon/h^2 + 1
    # u_{i+1}: epsilon/h^2 + (1+epsilon)/(2h)
    
    c_prev = epsilon/(h**2) - (1+epsilon)/(2*h)
    c_curr = -2*epsilon/(h**2) + 1.0
    c_next = epsilon/(h**2) + (1+epsilon)/(2*h)
    
    for i in range(dim):
        A[i, i] = c_curr
        if i > 0:     A[i, i-1] = c_prev
        if i < dim-1: A[i, i+1] = c_next
        
    # 邊界條件 u(0)=0 (無影響), u(1)=1 (移項到 b)
    b[dim-1] -= c_next * 1.0
    
    u_inner = np.linalg.solve(A, b)
    u_sol = np.concatenate(([0], u_inner, [1]))
    
    return x, u_sol

# --- 比較兩種網格密度 ---
# Case 1: N=20 (h=0.05)。因為 h > epsilon，預期會震盪失敗
x_20, u_20 = solve_sp_fdm(N=20)

# Case 2: N=200 (h=0.005)。因為 h < epsilon，預期準確
x_200, u_200 = solve_sp_fdm(N=200)

u_true = exact_solution(x_200)

# --- 誤差顯示 ---
err_20 = np.max(np.abs(exact_solution(x_20) - u_20))
err_200 = np.max(np.abs(exact_solution(x_200) - u_200))
print(f"Max Error (N=20) : {err_20:.4e} (Severe Oscillation!)")
print(f"Max Error (N=200): {err_200:.4e}")

# --- 繪圖 ---
plt.figure(figsize=(10, 6))
plt.plot(x_200, u_true, 'k-', linewidth=2, alpha=0.5, label='Exact Solution')
plt.plot(x_20, u_20, 'b-o', label='FDM N=20 (h=0.05 > $\epsilon$)')
plt.plot(x_200, u_200, 'r--', label='FDM N=200 (h=0.005 < $\epsilon$)')

plt.title(r'Exact vs FDM ($\epsilon=0.01$)')
plt.xlabel('x')
plt.ylabel('u(x)')
plt.legend()
plt.grid(True)
plt.show()

