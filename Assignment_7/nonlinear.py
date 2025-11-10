import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import root
from scipy.sparse import diags

def solve_bvp_fdm(N):
    """
    Solves the nonlinear BVP u'' = sin(u) using FDM.
    BCs: u(0) = 1, u(1) = 1
    N: Number of grid *intervals*
    """
    
    # 1. Setup grid
    h = 1.0 / N  # Step size
    num_unknowns = N - 1
    x = np.linspace(0, 1, N + 1)
    
    # Boundary conditions
    u_a = 1.0  # u(0)
    u_b = 1.0  # u(1)
    h2 = h * h

    # 2. Define the nonlinear system F(U) = 0
    def F(U):
        F_vec = np.zeros(num_unknowns)
        # i = 1
        F_vec[0] = u_a - 2 * U[0] + U[1] - h2 * np.sin(U[0])
        # i = 2 to N-2
        for i in range(1, num_unknowns - 1):
            F_vec[i] = U[i-1] - 2 * U[i] + U[i+1] - h2 * np.sin(U[i])
        # i = N-1
        F_vec[-1] = U[-2] - 2 * U[-1] + u_b - h2 * np.sin(U[-1])
        return F_vec

    # 3. Define the Jacobian matrix J(U)
    def J(U):
        diag_main = -2.0 - h2 * np.cos(U)
        diag_upper = np.ones(num_unknowns - 1)
        diag_lower = np.ones(num_unknowns - 1)
        J_matrix = diags([diag_lower, diag_main, diag_upper], 
                         [-1, 0, 1], 
                         shape=(num_unknowns, num_unknowns)).toarray()
        return J_matrix

    # 4. Initial guess
    U_guess = np.ones(num_unknowns)
    
    # 5. Solve the system
    sol = root(F, U_guess, jac=J, method='lm')
    
    if not sol.success:
        print(f"Solver failed for N={N}: {sol.message}")
        return None, None

    # 6. Assemble the full solution
    u_solution = np.concatenate(([u_a], sol.x, [u_b]))
    
    return x, u_solution

# --- Main Program ---

print("--- Starting Numerical Solution and Convergence Analysis ---")

# 1. Set N values for solutions and error analysis
N_values = [10, 20, 40, 80, 160] 
# Store all computed solutions for plotting and error analysis
all_solutions = {} 

# 2. Compute all solutions
print("\n--- Computing Solutions for Various Grid Sizes ---")
for N in N_values:
    x, u = solve_bvp_fdm(N)
    if u is not None:
        all_solutions[N] = {'x': x, 'u': u}
        print(f"Solution for N={N} computed.")
    else:
        print(f"Failed to compute solution for N={N}.")

# --- Plotting Numerical Solutions ---
plt.figure(figsize=(10, 6))
# Define some colors and markers for plotting
colors = ['b', 'g', 'r', 'c', 'm']
markers = ['o', 's', '^', 'D', 'x']

for i, N in enumerate(N_values):
    if N in all_solutions:
        plt.plot(all_solutions[N]['x'], all_solutions[N]['u'], 
                 marker=markers[i], markersize=5, linestyle='-', 
                 color=colors[i], label=f'N={N} (h={1/N:.3f})')

plt.xlabel('x', fontsize=14)
plt.ylabel('u(x)', fontsize=14)
plt.title('Numerical Solutions of Nonlinear BVP: $u\'\' = \sin(u)$', fontsize=16)
plt.legend(fontsize=12)
plt.grid(True)
plt.show() # Display the solution curves plot

# --- Log-Log Error Convergence Analysis ---
print("\n--- Running Log-Log Error Convergence Analysis ---")

h_values = []
errors = []

# Use the finest grid solution as reference
N_fine = N_values[-1]
x_fine = all_solutions[N_fine]['x']
u_fine = all_solutions[N_fine]['u']
print(f"Reference solution used: N={N_fine}.")

# Compute errors for coarser grids
for N in N_values[:-1]: # Iterate through N_values excluding the finest one
    h = 1.0 / N
    x_coarse = all_solutions[N]['x']
    u_coarse = all_solutions[N]['u']
    
    # Extract points from the fine solution that correspond to the coarse grid
    step = int(N_fine / N)
    u_fine_common_points = u_fine[::step]
    
    # Calculate L-infinity (max) error
    max_error = np.max(np.abs(u_coarse - u_fine_common_points))
    
    h_values.append(h)
    errors.append(max_error)
    print(f"N={N:3d} (h={h:.4f}): Max Error = {max_error:.6e}")

# Plot the Log-Log graph
plt.figure(figsize=(10, 7))
plt.loglog(h_values, errors, 'bo-', label='Numerical Error (L-infinity)', linewidth=2, markersize=8)

# Plot the O(h^2) reference line
C = errors[0] / (h_values[0]**2)
h_ref = np.array(h_values)
E_ref_O2 = C * (h_ref**2)
plt.loglog(h_ref, E_ref_O2, 'r--', label='Reference Slope $O(h^2)$ (Slope=2)', linewidth=2)

plt.xlabel('Step Size $h$', fontsize=14)
plt.ylabel('Max Error $E(h)$', fontsize=14)
plt.title('Log-Log Error Convergence Plot ($u\'\' = \sin(u)$)', fontsize=16)
plt.legend(fontsize=12)
plt.grid(True, which="both", ls="--")
plt.gca().invert_xaxis()
plt.show() # Display the log-log plot

# Optional: Calculate slope numerically
log_h = np.log(h_values)
log_E = np.log(errors)
slope, intercept = np.polyfit(log_h, log_E, 1)

print("\n--- Log-Log Slope Analysis ---")
print(f"The experimentally determined order of convergence (EOC) is: {slope:.6f}")
