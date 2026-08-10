import numpy as np
import matplotlib.pyplot as plt
from model import initialize_lattice, misfolded_fraction, monte_carlo_step

# ----------------------------------
# Baseline Configuration
# ----------------------------------
L = 50
f0 = 0.10
h = 0.0
T = 1.5
sweeps = 200
num_runs = 5  # Number of stochastic realizations per J

J_values = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0]

f_means = []
f_stds = []

print("=== Starting Parameter Sweep for J ===")
print(f"Grid: {L}x{L}, T: {T}, h: {h}, Sweeps: {sweeps}, Runs per J: {num_runs}\n")

for J in J_values:
    final_fractions = []
    
    for run in range(num_runs):
        lattice = initialize_lattice(L, misfolded_fraction=f0)
        
        for _ in range(sweeps):
            monte_carlo_step(lattice, T=T, J=J, h=h)
            
        final_fractions.append(misfolded_fraction(lattice))
    
    mean_f = np.mean(final_fractions)
    std_f = np.std(final_fractions) / np.sqrt(num_runs)  # Standard error
    
    f_means.append(mean_f)
    f_stds.append(std_f)
    
    print(f"J = {J:3.1f} | Final <f> = {mean_f:.4f} +/- {std_f:.4f}")

# ----------------------------------
# Plotting the Results
# ----------------------------------
plt.figure(figsize=(8, 5))
plt.errorbar(J_values, f_means, yerr=f_stds, fmt='-o', color='b', ecolor='r', capsize=5, label=r'$\langle f_{final} \rangle$')
plt.axhline(y=f0, color='gray', linestyle='--', label=f'Initial $f_0 = {f0}$')

plt.title(f'Parameter Sweep: Misfolded Fraction vs J (T={T})')
plt.xlabel('Interaction Strength (J)')
plt.ylabel('Final Misfolded Fraction $\langle f \\rangle$')
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.tight_layout()

# Save plot
plt.savefig('sweep_J_vs_f.png', dpi=300)
print("\n=== Sweep Completed! Plot saved as 'sweep_J_vs_f.png' ===")
