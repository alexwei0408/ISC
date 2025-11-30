import numpy as np
import matplotlib.pyplot as plt

def get_exact_solution(x, t):
    """
    解析解 (Exact Solution)
    """
    term1 = np.exp(-np.pi**2 * t / 4) * np.sin(0.5 * np.pi * x)
    term2 = 0.5 * np.exp(-4 * np.pi**2 * t) * np.sin(2 * np.pi * x)
    return term1 + term2

def compute_error_for_N(N, mu=0.5, T_end=0.1):
    """
    針對特定的網格數 N，執行模擬並回傳 L2 誤差
    """
    L = 1.0
    dx = L / N
    x = np.linspace(0, L, N+1)
    
    # 根據 mu 固定比例計算 dt (保證穩定性並連結空間與時間誤差)
    # dt = mu * dx^2
    dt = mu * dx**2
    time_steps = int(np.ceil(T_end / dt))
    
    # 重新調整 dt 確保剛好走到 T_end
    dt = T_end / time_steps 
    # 注意：微調 dt 可能會讓 mu 略微變動，但在 N 很大時差異可忽略
    # 這裡為了嚴謹，實際 mu = dt/dx^2 仍需滿足穩定條件 (通常變小，所以安全)

    # 初始化
    u = np.sin(0.5 * np.pi * x) + 0.5 * np.sin(2 * np.pi * x)
    u_curr = u.copy()
    u_next = np.zeros_like(u)
    
    t = 0
    # 時間迭代
    for n in range(time_steps):
        t += dt
        
        # Explicit Euler 核心
        # 使用切片操作加速運算
        u_next[1:-1] = u_curr[1:-1] + mu * (u_curr[2:] - 2*u_curr[1:-1] + u_curr[0:-2])
        
        # 邊界條件
        u_next[0] = 0
        u_next[-1] = np.exp(-np.pi**2 * t / 4)
        
        u_curr = u_next.copy()
        
    # 計算解析解
    u_exact = get_exact_solution(x, t)
    
    # 計算 L2 Error (Root Mean Square Error)
    # error = sqrt( sum((u_num - u_true)^2) / N )
    error = np.sqrt(np.mean((u_curr - u_exact)**2))
    
    return error

# --- 主程式：收斂性測試 ---

# 1. 設定一系列的 N 值 (從粗網格到細網格)
N_values = [10, 20, 40, 80, 160, 320]
errors = []

print(f"{'N':<10} | {'L2 Error':<15} | {'Order':<10}")
print("-" * 40)

# 2. 迴圈計算每個 N 的誤差
for i, N in enumerate(N_values):
    err = compute_error_for_N(N, mu=0.5, T_end=0.1)
    errors.append(err)
    
    # 計算收斂階數 (Slope)
    order = 0.0
    if i > 0:
        # Slope = log(E2/E1) / log(N1/N2)  (因為 N 變大，dx 變小)
        # 或者 log(E2/E1) / log(dx2/dx1)
        # 這裡 N_ratio = N[i] / N[i-1] = 2
        # Error_ratio = errors[i] / errors[i-1]
        order = - np.log(errors[i] / errors[i-1]) / np.log(N_values[i] / N_values[i-1])
        
    print(f"{N:<10} | {err:.2e}        | {order:.2f}")

# --- 3. 繪製 Log-Log 圖 ---
plt.figure(figsize=(8, 6))

# 畫出誤差數據點
plt.loglog(N_values, errors, 'bo-', linewidth=2, label='L2 Error (Forward Euler)')

# 畫出參考線 (Slope = -2, 即二階收斂)
# 因為我們固定 mu = dt/dx^2，所以 dt ~ O(dx^2)
# 總誤差 = O(dt) + O(dx^2) = O(dx^2) + O(dx^2) = O(dx^2)
# 所以我們預期看到斜率為 -2
ref_line = [errors[0] * (float(N_values[0])/n)**2 for n in N_values]
plt.loglog(N_values, ref_line, 'k--', label='Reference Slope -2 ($O(\Delta x^2)$)')

plt.xlabel('Number of Grid Points ($N$)')
plt.ylabel('L2 Error ($||u_{num} - u_{exact}||_2$)')
plt.title('Convergence Analysis (Log-Log Plot)')
plt.grid(True, which="both", ls="-", alpha=0.5)
plt.legend()

plt.show()
