import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import dst, idst

def solve_mol_fst_exact(N, T_end):
    """
    Method of Lines using FST with Exact Time Integration
    u_t = u_xx
    """
    # 1. 網格設置
    dx = 1.0 / N
    x_interior = np.linspace(dx, 1-dx, N-1)
    
    # 2. 初始條件 u(x, 0)
    u_0 = np.sin(2 * np.pi * x_interior) * np.exp(x_interior)
    
    # 3. 轉到頻域 (Forward DST)
    # 得到 u_hat(0)
    u_hat_0 = dst(u_0, type=1)
    
    # 4. 計算離散算子的特徵值 lambda_k
    # 這是矩陣 -1/dx^2 * A 的特徵值
    k = np.arange(1, N)
    lambda_k = (2 * np.cos(k * np.pi / N) - 2) / (dx**2)
    
    # 5. Method of Lines 的核心：在頻域直接求解 ODE
    # d(u_hat)/dt = lambda * u_hat  =>  u_hat(T) = u_hat(0) * exp(lambda * T)
    # 這一步在時間上是"精確"的 (Exact Time Integration)
    u_hat_T = u_hat_0 * np.exp(lambda_k * T_end)
    
    # 6. 轉回時域 (Inverse DST)
    u_final = idst(u_hat_T, type=1)
    
    return x_interior, u_final

def analyze_convergence():
    T_target = 1.0
    # 測試網格數
    N_values = [16, 32, 64, 128, 256]
    errors = []
    
    # 1. 計算參考解 (使用極高解析度)
    print(f"Computing reference solution at T={T_target} (N=2048)...")
    # 注意：T=1時解非常小，需要高精度計算
    _, u_ref_vals = solve_mol_fst_exact(2048, T_target)
    
    print(f"{'N':<10} | {'L2 Error':<15} | {'Order':<10}")
    print("-" * 40)

    for i, N in enumerate(N_values):
        # 計算當前 N 的解
        x, u = solve_mol_fst_exact(N, T_target)
        
        # 對齊參考解 (Downsampling)
        step = 2048 // N
        u_ref_aligned = u_ref_vals[step-1::step]
        
        # 計算 L2 Error
        error = np.sqrt(np.mean((u - u_ref_aligned)**2))
        errors.append(error)
        
        # 計算 Order
        order = 0.0
        if i > 0:
            order = np.log(errors[i-1] / errors[i]) / np.log(N_values[i] / N_values[i-1])
        
        print(f"{N:<10} | {error:.2e}        | {order:.2f}")

    # 繪圖
    plt.figure(figsize=(10, 6))
    
    # 繪製解的形狀 (取 N=256)
    plt.subplot(1, 2, 1)
    x_plot, u_plot = solve_mol_fst_exact(64, T_target)
    plt.plot(x_plot, u_plot, 'b-', label=f'u(x, T={T_target})')
    plt.title(f'Solution Profile at T={T_target}')
    plt.xlabel('x')
    plt.ylabel('u')
    plt.grid(True)
    # 標註解的大小，讓使用者知道數值很小
    plt.text(0.5, np.max(u_plot)*0.8, f'Max value ~ {np.max(u_plot):.2e}', ha='center')

    # 繪製收斂圖
    plt.subplot(1, 2, 2)
    plt.loglog(N_values, errors, 'o-', label='L2 Error')
    # 參考斜率 2
    ref_line = [errors[0] * (N_values[0]/n)**2 for n in N_values]
    plt.loglog(N_values, ref_line, 'k--', label='Slope -2 (O(dx^2))')
    
    plt.xlabel('N')
    plt.ylabel('Error')
    plt.title('Spatial Convergence')
    plt.legend()
    plt.grid(True, which="both", ls="-")
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    analyze_convergence()
