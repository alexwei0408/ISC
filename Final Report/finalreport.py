import numpy as np
import matplotlib.pyplot as plt
from scipy.special import roots_legendre
from scipy.interpolate import lagrange

class SDC_Solver:
    def __init__(self, m, t_start, t_end):
        """
        初始化 SDC solver
        m: Gauss-Legendre 節點數量
        t_start, t_end: 時間區間
        """
        self.m = m
        self.t_start = t_start
        self.t_end = t_end
        
        # 1. 取得 Gauss-Legendre 節點 (原本在 [-1, 1])
        r, _ = roots_legendre(m)
        self.r = np.sort(r) # 排序節點
        
        # 2. 將節點映射到 [t_start, t_end] -> s nodes
        # 根據論文，我們在 s_1...s_m 上求解，但也需要起始點 t_0
        self.s = 0.5 * (self.t_end - self.t_start) * self.r + 0.5 * (self.t_end + self.t_start)
        self.nodes = np.concatenate(([self.t_start], self.s)) # [t_0, s_1, ..., s_m]
        
        # 3. 建構積分矩陣 S_matrix
        # S_ij = int_{t_start}^{s_i} L_j(tau) dtau
        # 我們需要對 Lagrange 基底多項式進行積分
        self.S_matrix = self._compute_integration_matrix()

    def _compute_integration_matrix(self):
        """
        計算積分矩陣 S。
        S[i, j] 代表第 j 個 Lagrange 基底函數從 t_start 到 node[i+1] 的積分。
        """
        S = np.zeros((self.m, self.m))
        
        # 這裡僅使用 Gauss 節點 s 來構建 Lagrange 多項式
        # 注意：論文中 Lagrange 插值通常是基於 m 個 Gauss 節點
        
        for j in range(self.m):
            # 建立第 j 個節點的 Lagrange 基底多項式 L_j(t)
            # 這裡簡單使用 scipy 的 lagrange，雖然數值上不是最優但對小 m 足夠
            y_dummy = np.zeros(self.m)
            y_dummy[j] = 1.0
            poly = lagrange(self.s, y_dummy)
            poly_integ = poly.integ() # 不定積分
            
            for i in range(self.m):
                # 計算定積分：從 t_start 到 s[i]
                val = poly_integ(self.s[i]) - poly_integ(self.t_start)
                S[i, j] = val
        return S

    def solve(self, f, lambda_val, y0, J_sweeps):
        """
        執行 SDC 疊代
        f: 函數 f(t, y) = lambda * y
        lambda_val: 特徵值 (例如 -100)
        y0: 初始值
        J_sweeps: 校正次數
        """
        # 初始化解向量 (包含 t0)
        y = np.zeros(self.m + 1)
        y[0] = y0
        
        # === 步驟 1: 預測 (Prediction) ===
        # 使用隱式歐拉法 (Implicit Euler) 計算初始猜測值
        # y_{k+1} = y_k + h * lambda * y_{k+1}  =>  y_{k+1} = y_k / (1 - h * lambda)
        for i in range(self.m):
            dt = self.nodes[i+1] - self.nodes[i]
            y[i+1] = y[i] / (1 - dt * lambda_val)
            
        y_initial_guess = y.copy()

        # === 步驟 2: 延遲校正 (Deferred Correction) ===
        for sweep in range(J_sweeps):
            # A. 計算殘差 (Residual)
            # epsilon(t) = y_0 + int(F(y)) - y
            # 計算 F(y) 在所有 Gauss 節點上的值 (不包含 t0)
            F_vals = f(self.s, y[1:]) 
            
            # 使用積分矩陣計算積分值
            Integrals = self.S_matrix @ F_vals
            
            # 計算殘差 epsilon (在每個 Gauss 節點上)
            # epsilon_vec[i] 對應節點 s[i]
            epsilon_vec = y[0] + Integrals - y[1:]
            
            # 為了方便掃描，我們在 epsilon 前面補上 0 (對應 t0 的殘差為 0)
            epsilon_full = np.concatenate(([0.0], epsilon_vec))
            
            # B. 求解誤差方程 (Error Equation)
            # delta' = lambda * delta + (epsilon' term)
            # 離散化: delta_{i+1} = delta_i + h * lambda * delta_{i+1} + (epsilon_{i+1} - epsilon_i)
            # 移項: delta_{i+1} * (1 - h * lambda) = delta_i + (epsilon_{i+1} - epsilon_i)
            
            delta = np.zeros(self.m + 1) # delta[0] = 0
            
            for i in range(self.m):
                dt = self.nodes[i+1] - self.nodes[i]
                rhs = delta[i] + (epsilon_full[i+1] - epsilon_full[i])
                delta[i+1] = rhs / (1 - dt * lambda_val)
            
            # C. 更新解
            y = y + delta
            
        return self.nodes, y, y_initial_guess

# === 主程式參數設定 ===
lambda_val = -100   # 剛性係數 (Stiffness)
y0 = 1.0            # 初始條件
T_end = 0.2         # 模擬總時間 (不需要很長即可看到剛性影響)
m_nodes = 5         # Gauss-Legendre 節點數
J_sweeps = 5        # 校正次數

# 定義 ODE 函數
def ode_func(t, y):
    return lambda_val * y

# 1. 執行 SDC (Implicit)
sdc = SDC_Solver(m_nodes, 0, T_end)
t_sdc, y_sdc, y_pred = sdc.solve(ode_func, lambda_val, y0, J_sweeps)

# 2. 解析解 (Exact Solution)
t_fine = np.linspace(0, T_end, 100)
y_exact = y0 * np.exp(lambda_val * t_fine)

# 3. 顯式歐拉 (Explicit Euler) - 用作對照組
# 故意使用與 SDC 平均步長相似的步長，展示其不穩定性
dt_explicit = T_end / m_nodes 
t_explicit = [0]
y_explicit = [y0]
curr_y = y0
for _ in range(m_nodes):
    curr_y = curr_y + dt_explicit * (lambda_val * curr_y)
    y_explicit.append(curr_y)
    t_explicit.append(t_explicit[-1] + dt_explicit)

# === 繪圖結果 ===
plt.figure(figsize=(10, 6))

# 畫解析解
plt.plot(t_fine, y_exact, 'k-', alpha=0.6, label='Exact Solution', linewidth=2)

# 畫顯式歐拉 (通常會震盪或發散)
plt.plot(t_explicit, y_explicit, 'r--o', label=f'Explicit Euler (N={m_nodes})', linewidth=1.5)

# 畫 SDC 預測 (低階隱式)
plt.plot(t_sdc, y_pred, 'g--x', label='SDC Prediction (Implicit Euler)', alpha=0.5)

# 畫 SDC 最終結果 (高階隱式)
plt.plot(t_sdc, y_sdc, 'b-d', label=f'SDC Final (m={m_nodes}, J={J_sweeps})', linewidth=2, markersize=8)

plt.title(f"Solving Stiff ODE: y' = {lambda_val}y\nImplicit SDC vs Explicit Euler")
plt.xlabel("Time t")
plt.ylabel("y(t)")
plt.legend()
plt.grid(True)
plt.ylim(min(min(y_explicit), -0.5), max(max(y_explicit), 1.5)) # 限制 y 軸避免顯式歐拉發散太遠導致看不清
plt.show()

# 輸出數值比較
print(f"{'Time':<10} {'Exact':<15} {'Explicit':<15} {'SDC Final':<15}")
print("-" * 55)
for i in range(len(t_sdc)):
    exact_val = y0 * np.exp(lambda_val * t_sdc[i])
    # 找最接近的 explicit 值 (僅供參考)
    print(f"{t_sdc[i]:<10.4f} {exact_val:<15.5f} {'(Unstable)':<15} {y_sdc[i]:<15.5f}")
