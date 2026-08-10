import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from model import (
    initialize_lattice,
    misfolded_fraction,
    monte_carlo_step
)

# ==================================
# Refinement Configuration
# ==================================

L = 50
N = L * L
f0 = 0.10

J = 1.0
h = 0.2

# Fine temperature grid in the candidate region
T_values = np.linspace(2.0, 2.8, 17)  # Step = 0.05

sweeps = 200
num_runs = 20  # Increased for statistically robust variance calculation

# ==================================
# Run Simulation
# ==================================

print("=== Starting Temperature Refinement & Susceptibility Measurement ===")
print(f"Grid: {L}x{L} (N={N}) | J: {J} | h: {h}")
print(f"Sweeps: {sweeps} | Runs per T: {num_runs}\n")

f_means = []
f_sems = []
f_vars = []
chi_f_list = []

for T in T_values:
    final_fractions = []
    
    for run in range(num_runs):
        lattice = initialize_lattice(L, misfolded_fraction=f0)
        
        for _ in range(sweeps):
            monte_carlo_step(lattice, T=T, J=J, h=h)
            
        final_fractions.append(misfolded_fraction(lattice))
    
    # Statistical measures
    mean_f = np.mean(final_fractions)
    std_f = np.std(final_fractions, ddof=1)
    sem_f = std_f / np.sqrt(num_runs)
    
    # Variance & Susceptibility
    var_f = np.var(final_fractions, ddof=1)
    chi_f = (N / T) * var_f
    
    f_means.append(mean_f)
    f_sems.append(sem_f)
    f_vars.append(var_f)
    chi_f_list.append(chi_f)
    
    print(f"T = {T:4.2f} | <f> = {mean_f:.4f} +/- {sem_f:.4f} | Var(f) = {var_f:.6f} | chi_f = {chi_f:.4f}")

# ==================================
# Save Results
# ==================================

results_dir = "results"
os.makedirs(results_dir, exist_ok=True)

df = pd.DataFrame({
    "T": T_values,
    "mean_f": f_means,
    "sem_f": f_sems,
    "var_f": f_vars,
    "chi_f": chi_f_list,
    "J": [J] * len(T_values),
    "h": [h] * len(T_values),
    "L": [L] * len(T_values),
    "num_runs": [num_runs] * len(T_values)
})

csv_path = os.path.join(results_dir, "T_refinement_J1.0_h0.2.csv")
df.to_csv(csv_path, index=False)

# ==================================
# Plotting (2-Panel Figure)
# ==================================

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 9), sharex=True)

# Panel 1: <f> vs T
ax1.errorbar(T_values, f_means, yerr=f_sems, fmt="-o", color="tab:blue", capsize=4, label=r"$\langle f \rangle$")
ax1.axhline(y=f0, linestyle="--", color="gray", label=f"Initial $f_0={f0}$")
ax1.set_ylabel(r"Final Misfolded Fraction $\langle f \rangle$")
ax1.set_title(f"Temperature Refinement & Susceptibility\n$J={J},\\ h={h},\\ L={L},\\ N_{\\mathrm{{runs}}}={num_runs}$")
ax1.grid(True, linestyle=":", alpha=0.6)
ax1.legend()

# Panel 2: Susceptibility chi_f vs T
ax2.plot(T_values, chi_f_list, "-s", color="tab:red", label=r"$\chi_f = \frac{N}{T} \mathrm{Var}(f)$")
ax2.set_xlabel("Temperature T")
ax2.set_ylabel(r"Susceptibility $\chi_f$")
ax2.grid(True, linestyle=":", alpha=0.6)
ax2.legend()

plt.tight_layout()

plot_path = os.path.join(results_dir, "T_refinement_J1.0_h0.2.png")
plt.savefig(plot_path, dpi=300)

print("\n=== Refinement Completed ===")
print(f"CSV saved to: {csv_path}")
print(f"Plot saved to: {plot_path}")
