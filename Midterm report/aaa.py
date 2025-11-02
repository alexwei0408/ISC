import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import svd
import platform
import matplotlib.font_manager as fm
# 導入泰勒級數所需的函式
from scipy.interpolate import approximate_taylor_polynomial

# Define the Runge function
# ... (aaa_simple 函式和 eval_rational 函式保持不變) ...
def runge(z):
    return 1 / (1 + 25*z**2)

# AAA Algorithm Implementation (simplified version)
def aaa_simple(F, Z, tol=1e-10, mmax=20):
    M = len(Z)
    F = np.array(F)
    Z = np.array(Z)
    
    # Initialize
    J = list(range(M))  # Unused indices
    z = []  # Support points
    f = []  # Function values at support points
    errors = []
    
    # Mean as initial approximation
    R = np.full(M, np.mean(F))
    
    for m in range(mmax):
        # 1. Greedy selection of support point
        residual = np.abs(F[J] - R[J])
        j_local = np.argmax(residual)
        j = J[j_local]
        
        # Add new support point
        z.append(Z[j])
        f.append(F[j])
        J.remove(j)
        
        if len(J) == 0:
            break
        
        # 2. Build Cauchy matrix C
        Z_unused = Z[J]
        C = 1 / (Z_unused[:, np.newaxis] - np.array(z))
        
        # 3. Build Loewner matrix
        F_unused = F[J]
        SF = np.diag(F_unused)
        Sf = np.diag(f)
        A = SF @ C - C @ Sf
        
        # 4. Solve for weights using SVD
        U, s, Vh = svd(A, full_matrices=False)
        w = Vh[-1, :].conj()  # Last right singular vector
        
        # 5. Form rational approximant
        N = C @ (w * f)
        D = C @ w
        R[J] = N / D
        
        # 6. Compute error
        err = np.max(np.abs(F[J] - R[J]))
        errors.append(err)
        
        # 7. Check convergence
        if err <= tol * np.max(np.abs(F)):
            break
    
    return np.array(z), np.array(f), w, errors

# Evaluate the rational approximation
def eval_rational(z_eval, z_support, f_support, w):
    """
    Evaluate rational approximation in barycentric form
    """
    z_eval = np.atleast_1d(z_eval)
    result = np.zeros_like(z_eval, dtype=complex)
    
    for i, ze in enumerate(z_eval):
        # Avoid division by zero at support points
        if np.any(np.abs(ze - z_support) < 1e-14):
            idx = np.argmin(np.abs(ze - z_support))
            result[i] = f_support[idx]
        else:
            cauchy = 1 / (ze - z_support)
            N = np.sum(w * f_support * cauchy)
            D = np.sum(w * cauchy)
            result[i] = N / D
    
    return result.real if np.all(np.isreal(result)) else result

print("=" * 60)
print("AAA ALGORITHM DEMONSTRATION")
print("=" * 60)
print("\nApproximating the Runge function: f(x) = 1/(1 + 25x²)")
print("on the interval [-1, 1]\n")

# Sample the Runge function
M = 100  # Number of sample points
Z_sample = np.linspace(-1, 1, M)
F_sample = runge(Z_sample)

# Run AAA algorithm
z_support, f_support, w, errors = aaa_simple(F_sample, Z_sample, tol=1e-10, mmax=20)

print(f"Number of support points selected: {len(z_support)}")
print(f"Final approximation error: {errors[-1]:.2e}")
print(f"\nSupport points locations:")
for i, zs in enumerate(z_support[:5]):  # Show first 5
    print(f"  z[{i+1}] = {zs:.4f}")
if len(z_support) > 5:
    print(f"  ... and {len(z_support)-5} more points")

print(f"\nConvergence history:")
for i, err in enumerate(errors[:10]):
    print(f"  Iteration {i+1}: error = {err:.2e}")
if len(errors) > 10:
    print(f"  ... ({len(errors)-10} more iterations)")

# Evaluate on a fine grid for plotting
x_fine = np.linspace(-1, 1, 500)
f_true = runge(x_fine)
f_approx = eval_rational(x_fine, z_support, f_support, w)

# Compute pointwise error
pointwise_error = np.abs(f_true - f_approx)
max_error = np.max(pointwise_error)

print(f"\nMaximum error on fine grid (AAA): {max_error:.2e}")
print(f"Rational approximation type: ({len(z_support)-1}, {len(z_support)-1})")


# --- 泰勒級數計算 (Taylor Expansion) ---
# 為了公平比較，使用與 AAA 相同的階數
degree = len(z_support) - 1
# 在 z=0 點展開
# 確保 order > degree 
taylor_poly = approximate_taylor_polynomial(runge, 0, degree=degree, scale=1.0, order=degree + 2)
f_taylor = taylor_poly(x_fine)

# 計算泰勒級數的誤差
taylor_pointwise_error = np.abs(f_true - f_taylor)
taylor_max_error = np.max(taylor_pointwise_error)

print(f"Maximum error on fine grid (Taylor): {taylor_max_error:.2e}")
print(f"Taylor polynomial degree: {degree}")
print("\n" + "=" * 60)


# === 繪圖 (Plotting) ===

# --- 移除中文字體設定 ---
# (Font settings removed as titles are now in English)
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
# --- 設定結束 ---


# 調整圖表大小為 2 個子圖
plt.figure(figsize=(12, 6))

# --- 圖 1: 函數逼近 ---
plt.subplot(1, 2, 1) # 改為 1, 2, 1
plt.plot(x_fine, f_true, 'k-', linewidth=2, label='True Function (Runge)')
plt.plot(x_fine, f_approx.real, 'r--', label=f'AAA Approx. (m={len(z_support)})') 
# 加入泰勒級數
plt.plot(x_fine, f_taylor, 'b:', label=f'Taylor Approx. (degree={degree})') 
plt.scatter(z_support, f_support.real, c='blue', s=40, zorder=5, label='Support Points')
plt.title('Function Approximation')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.ylim(-0.5, 1.5) # 限制 y 軸，因為泰勒級數會發散
plt.grid(True)

# --- 圖 2: 逐點誤差 (Semilogy) ---
plt.subplot(1, 2, 2) # 改為 1, 2, 2
plt.semilogy(x_fine, pointwise_error, 'r-', label='AAA Error')
# 加入泰勒級數的誤差
plt.semilogy(x_fine, taylor_pointwise_error, 'b-', label=f'Taylor Error (degree={degree})')
plt.title('Pointwise Error (Log Scale)')
plt.xlabel('x')
plt.ylabel('log|f(x) - r(x)|')
plt.legend()
plt.grid(True)

