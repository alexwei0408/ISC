import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad, solve_ivp

# --- 1. 計算 alpha ---
def source_f(x):
    return np.exp(np.sin(x))

# 數值積分算出 alpha
alpha_val, _ = quad(source_f, 0, 1)
print(f"Calculated alpha = {alpha_val:.8f}")

# --- 2. 產生「真值解」 (Reference Solution) ---
# 因為沒有解析解公式，我們用高精度 ODE Solver (RK45) 產生對照組
# 轉換為一階系統: y1' = y2, y2' = f(x)
# IC: y1(0)=0 (我們選定通過原點的那個解), y2(0)=0 (題目給定 u'(0)=0)
def ode_system(t, y):
    return [y[1], source_f(t)]

sol = solve_ivp(ode_system, [0, 1], [0, 0], t_eval=np.linspace(0, 1, 321), rtol=1e-13)
x_true = sol.t
u_true = sol.y[0]

# --- 3. FDM 求解 ---
def solve_fdm_neumann_inhomogeneous(N, alpha):
    h = 1.0 / N
    x = np.linspace(0, 1, N+1)
    dim = N + 1
    A = np.zeros((dim, dim))
    b = np.zeros(dim)
    
    # 內部節點
    for i in range(1, N):
        A[i, i-1] = 1.0
        A[i, i]   = -2.0
        A[i, i+1] = 1.0
        b[i]      = (h**2) * source_f(x[i])
        
    # 左邊界 i=0 (u'(0)=0)
    # Ghost point: -2u0 + 2u1 = h^2 f(0)
    A[0, 0] = -2.0
    A[0, 1] = 2.0
    b[0]    = (h**2) * source_f(x[0])
    
    # 右邊界 i=N (u'(1)=alpha)
    # Ghost point: 2u_{N-1} - 2u_N = h^2 f(1) - 2h*alpha
    A[N, N-1] = 2.0
    A[N, N]   = -2.0
    b[N]      = (h**2) * source_f(x[N]) - 2 * h * alpha
    
    # 求解奇異矩陣 (Singular Matrix)
    # 使用 Least Squares 求解
    u_sol, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
    
    # 平移解：強制讓 u(0) = 0 與真值比較
    u_sol = u_sol - u_sol[0]
    
    return x, u_sol

# 執行計算 N=40
N_grid = 40
x_fdm, u_fdm = solve_fdm_neumann_inhomogeneous(N_grid, alpha_val)

sol_check = solve_ivp(ode_system, [0, 1], [0, 0], t_eval=x_fdm, rtol=1e-13)
u_true_at_nodes = sol_check.y[0]
error = u_fdm - u_true_at_nodes

# --- 繪圖 ---
plt.figure(figsize=(12, 5))

# 子圖 1: 解
plt.subplot(1, 2, 1)
plt.plot(x_true, u_true, 'k-', label='Exact (via ODE45)')
plt.plot(x_fdm, u_fdm, 'ro--', label=f'FDM (N={N_grid})')
plt.title(f"Solution u(x) with $\\alpha \\approx {alpha_val:.4f}$")
plt.xlabel('x')
plt.ylabel('u(x)')
plt.legend()
plt.grid(True)

# 子圖 2: 誤差
plt.subplot(1, 2, 2)
plt.plot(x_fdm, error, 'b.-')
plt.title(f"Pointwise Error (Numeric - Exact), N={N_grid}")
plt.xlabel('x')
plt.grid(True)

plt.tight_layout()
plt.show()

print(f"Max Error (N={N_grid}): {np.max(np.abs(error)):.4e}")
