import numpy as np
import matplotlib.pyplot as plt

def solve_diffusion(mu, N=20, T_end=1.0):
    L = 1.0
    dx = L / N
    x = np.linspace(0, L, N+1)
    
    dt = mu * dx**2
    time_steps = int(T_end / dt)
    
    # 2. 初始化 u 陣列
    # Initial Condition: u(x,0)
    u = np.sin(0.5 * np.pi * x) + 0.5 * np.sin(2 * np.pi * x)
    
    # 用來存儲不同時間點的解以便繪圖
    u_history = [u.copy()]
    t_history = [0]
    
    t = 0
    u_curr = u.copy()
    u_next = np.zeros_like(u)
    
    # 3. 時間迭代
    for n in range(time_steps):
        t += dt
        
        # 內點計算 (Forward Euler)
        # u_next[j] = mu*u[j+1] + (1-2mu)*u[j] + mu*u[j-1]
        u_next[1:-1] = mu * u_curr[2:] + (1 - 2*mu) * u_curr[1:-1] + mu * u_curr[0:-2]
        
        # 邊界條件 (Boundary Conditions)
        u_next[0] = 0  # 左邊界
        u_next[-1] = np.exp(-np.pi**2 * t / 4)  # 右邊界 (Time dependent)
        
        # 更新狀態
        u_curr = u_next.copy()
        
        # 存儲數據 (為了避免存太多，每隔一段時間存一次)
        if (n+1) % (time_steps // 5) == 0 or n == time_steps - 1:
            u_history.append(u_curr.copy())
            t_history.append(t)
            
    return x, u_history, t_history

# --- 執行兩種情況 ---

# Case 1: Stable (mu = 0.5)
x1, u_hist1, t_hist1 = solve_diffusion(mu=0.5)

# Case 2: Unstable (mu = 0.509)
x2, u_hist2, t_hist2 = solve_diffusion(mu=0.509)

# --- 繪圖比較 ---
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot Case 1
ax = axes[0]
for i, u in enumerate(u_hist1):
    ax.plot(x1, u, label=f't={t_hist1[i]:.2f}')
ax.set_title(r'Case 1: $\mu=0.5$ (Stable)')
ax.set_xlabel('x')
ax.set_ylabel('u')
ax.grid(True)
ax.legend()

# Plot Case 2
ax = axes[1]
for i, u in enumerate(u_hist2):
    ax.plot(x2, u, label=f't={t_hist2[i]:.2f}')
ax.set_title(r'Case 2: $\mu=0.509$ (Unstable)')
ax.set_xlabel('x')
ax.grid(True)
ax.legend()

plt.tight_layout()
plt.show()
