import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

def solve_bvp_linear(N):
    """
    使用 FDM 求解線性 BVP: -u'' = exp(sin(x))
    N: 網格 *區間* 的數量
    """
    
    # 1. 設置網格
    h = 1.0 / N
    
    # 內部節點 (i=1 to N-1)
    x_internal = np.linspace(h, 1.0 - h, N - 1)
    
    # 完整節點 (i=0 to N)
    x_full = np.linspace(0, 1.0, N + 1)
    
    # 2. 構建矩陣 A
    # 主對角線
    main_diag = np.full(N - 1, 2.0)
    # 次對角線
    off_diag = np.full(N - 2, -1.0)
    
    # 使用 diags 創建稀疏矩陣
    A = diags([off_diag, main_diag, off_diag], [-1, 0, 1], shape=(N - 1, N - 1))
    
    # 3. 構建向量 b
    f = np.exp(np.sin(x_internal))
    b = h**2 * f
    
    # 邊界條件 u(0)=0 和 u(1)=0 已經隱含在 b 的構建中
    
    # 4. 求解 A*u = b
    # 將 A 轉換為 CSC (Compressed Sparse Column) 格式以提高求解效率
    u_internal = spsolve(A.tocsc(), b)
    
    # 5. 組合完整解 (包含邊界)
    u_solution = np.concatenate(([0.0], u_internal, [0.0]))
    
    return x_full, u_solution

def compute_exact_solution(x_nodes):
    """
    計算給定 x 節點處的精確解
    u(x) = (1-x) * int_0^x (s * exp(sin(s))) ds + x * int_x^1 ((1-s) * exp(sin(s))) ds
    """
    
    # 定義積分項
    def integrand1(s):
        return s * np.exp(np.sin(s))
    
    def integrand2(s):
        return (1 - s) * np.exp(np.sin(s))
    
    u_exact_values = []
    
    # 遍歷所有 x 節點
    for x in x_nodes:
        # 使用 scipy.integrate.quad 進行高精度積分
        integral1, _ = integrate.quad(integrand1, 0, x)
        integral2, _ = integrate.quad(integrand2, x, 1)
        
        u_val = (1 - x) * integral1 + x * integral2
        u_exact_values.append(u_val)
        
    return np.array(u_exact_values)

# --- 1. 繪製數值解與精確解對比圖 ---

print("--- Plotting Solutions ---")
N_values_plot = [5, 10, 20] # 選擇幾個 N 值進行繪圖

# 創建一條高解析度的精確解曲線
x_true = np.linspace(0, 1, 200)
u_true = compute_exact_solution(x_true)

plt.figure(figsize=(10, 6))
plt.plot(x_true, u_true, 'k-', linewidth=2, label='Exact Solution')

# 繪製不同 N 值下的 FDM 解
for N in N_values_plot:
    x_fdm, u_fdm = solve_bvp_linear(N)
    plt.plot(x_fdm, u_fdm, 'o--', label=f'FDM N={N}')

plt.xlabel('x', fontsize=14)
plt.ylabel('u(x)', fontsize=14)
plt.title('Numerical FDM vs. Exact Solution for $-u\'\' = \exp(\sin(x))$', fontsize=16)
plt.legend(fontsize=12)
plt.grid(True)
plt.show()

# --- 2. 繪製 Log-Log 誤差收斂圖 ---

print("\n--- Running Log-Log Error Convergence Analysis ---")
N_values_error = [10, 20, 40, 80, 160]
h_values = []
errors = []

for N in N_values_error:
    h = 1.0 / N
    
    # 1. 計算 FDM 解
    x_fdm, u_fdm = solve_bvp_linear(N)
    
    # 2. 在 *相同* 的 FDM 網格點上計算精確解
    u_exact_on_grid = compute_exact_solution(x_fdm)
    
    # 3. 計算 L-infinity (最大) 誤差
    max_error = np.max(np.abs(u_fdm - u_exact_on_grid))
    
    h_values.append(h)
    errors.append(max_error)
    print(f"N={N:3d} (h={h:.4f}): Max Error = {max_error:.6e}")

# 繪製 Log-Log 圖
plt.figure(figsize=(10, 7))
plt.loglog(h_values, errors, 'bo-', label='Numerical Error (L-infinity)', linewidth=2, markersize=8)

# 繪製 O(h^2) 參考線
C = errors[0] / (h_values[0]**2)
h_ref = np.array(h_values)
E_ref_O2 = C * (h_ref**2)
plt.loglog(h_ref, E_ref_O2, 'r--', label='Reference Slope $O(h^2)$ (Slope=2)', linewidth=2)

plt.xlabel('Step Size $h$', fontsize=14)
plt.ylabel('Max Error $E(h)$', fontsize=14)
plt.title('Log-Log Error Convergence Plot (FDM vs. Exact Solution)', fontsize=16)
plt.legend(fontsize=12)
plt.grid(True, which="both", ls="--")
plt.gca().invert_xaxis()
plt.show()

# 數值計算收斂階
log_h = np.log(h_values)
log_E = np.log(errors)
slope, _ = np.polyfit(log_h, log_E, 1)

print("\n--- Log-Log Slope Analysis ---")
print(f"The experimentally determined order of convergence (EOC) is: {slope:.6f}")
