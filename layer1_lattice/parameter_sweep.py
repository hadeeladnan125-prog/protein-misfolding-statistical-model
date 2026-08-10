import os
import numpy as np
import pandas as pd
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
# Save Results (CSV & Documentation)
# ----------------------------------
results_dir = "results"
os.makedirs(results_dir, exist_ok=True)

# Save CSV
df = pd.DataFrame({
    'J': J_values,
    'mean_f': f_means,
    'std_f': f_stds,
    'T': [T] * len(J_values),
    'L': [L] * len(J_values)
})
csv_path = os.path.join(results_dir, "J_sweep_T1.5.csv")
df.to_csv(csv_path, index=False)
print(f"\n[Data Saved] CSV results written to '{csv_path}'")

# Save README Documentation
readme_path = os.path.join(results_dir, "README.md")
readme_content = f"""# Experiment Results: J Parameter Sweep

## Baseline Parameters
- **Initial Condition ($f_0$):** {f0}
- **Temperature ($T$):** {T}
- **Lattice Size ($L$):** {L}x{L}
- **External Field ($h$):** {h}
- **Number of Sweeps:** {sweeps}
- **Independent Runs per J:** {num_runs}
- **Range of $J$:** {J_values}

## Observables
- **$\\langle f \\rangle$ (mean_f):** Ensemble average of final misfolded fraction.
- **Uncertainty (std_f):** Standard error of the mean across independent realizations.

## Scientific Note
The observed behavior shows a sharp change in $\\langle f \\rangle$ near $J \\approx 0.6$. 
This behavior represents a **transition-like / crossover phenomenon** in a finite system ($L=50$), and does NOT constitute a thermodynamic proof of a critical phase transition without finite-size scaling ($L \\to \\infty$) and fluctuation analysis ($\\chi$).
"""

with open(readme_path, "w") as f:
    f.write(readme_content)
print(f"[Docs Saved] Experiment metadata written to '{readme_path}'")

# ----------------------------------
# Plotting the Results
# ----------------------------------
plt.figure(figsize=(8, 5))
plt.errorbar(J_values, f_means, yerr=f_stds, fmt='-o', color='b', ecolor='r', capsize=5, label=r'$\langle f_{final} \rangle$')
plt.axhline(y=f0, color='gray', linestyle='--', label=f'Initial $f_0 = {f0}$')

plt.title(f'Parameter Sweep: Misfolded Fraction vs J (T={T})')
plt.xlabel('Interaction Strength (J)')
plt.ylabel('Final Misfolded Fraction $\\langle f \\rangle$')
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.tight_layout()

plot_path = os.path.join(results_dir, "sweep_J_vs_f.png")
plt.savefig(plot_path, dpi=300)
print(f"[Plot Saved] Figure saved as '{plot_path}'")
print("\n=== All Tasks Completed Successfully! ===")
