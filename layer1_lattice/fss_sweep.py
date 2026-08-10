import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from model import (
    initialize_lattice,
    misfolded_fraction,
    monte_carlo_step
)

# ====================================================
# Finite-Size Exploratory Scan Configuration
# ====================================================

L_values = [20, 30, 50, 70, 100]
f0 = 0.10

J = 1.0
h = 0.2

# Temperature grid focused around the crossover window
T_values = np.linspace(2.2, 2.8, 13)  # Step = 0.05

sweeps = 200
num_runs = 15  # Independent runs per (L, T) point

# Storage for aggregate results
all_results = []

print("=== Starting Finite-Size Exploratory Scan (L-Sweep) ===")
print(f"Lattice Sizes (L): {L_values} | J: {J} | h: {h}")
print(f"Temperature Points: {len(T_values)} | Runs per point: {num_runs}\n")

# ====================================================
# Run Simulation Loop over L and T
# ====================================================

for L in L_values:
    N = L * L
    print(f"--- Running Lattice L = {L} (N = {N}) ---")
    
    for T in T_values:
        final_fractions = []
        
        for run in range(num_runs):
            lattice = initialize_lattice(L, misfolded_fraction=f0)
            
            for _ in range(sweeps):
                monte_carlo_step(lattice, T=T, J=J, h=h)
                
            final_fractions.append(misfolded_fraction(lattice))
        
        mean_f = np.mean(final_fractions)
        std_f = np.std(final_fractions, ddof=1)
        sem_f = std_f / np.sqrt(num_runs)
        
        # Inter-run variance and proxy susceptibility chi_f^(run)
        var_f = np.var(final_fractions, ddof=1)
        chi_f_run = (N / T) * var_f
        
        all_results.append({
            "L": L,
            "N": N,
            "T": T,
            "mean_f": mean_f,
            "sem_f": sem_f,
            "var_f": var_f,
            "chi_f_run": chi_f_run
        })
        
    print(f"L = {L} completed.")

df = pd.DataFrame(all_results)

# ====================================================
# Save Results
# ====================================================

results_dir = "results"
os.makedirs(results_dir, exist_ok=True)

csv_path = os.path.join(results_dir, "fss_L_sweep_results.csv")
df.to_csv(csv_path, index=False)

# ====================================================
# Plot 1: Misfolded Fraction <f> vs T
# ====================================================

colors = plt.cm.viridis(np.linspace(0.1, 0.9, len(L_values)))

plt.figure(figsize=(8, 6))
for idx, L in enumerate(L_values):
    sub_df = df[df["L"] == L]
    plt.errorbar(
        sub_df["T"], sub_df["mean_f"], yerr=sub_df["sem_f"],
        fmt="-o", color=colors[idx], label=f"L = {L}", capsize=3
    )

plt.axhline(y=f0, linestyle="--", color="gray", alpha=0.7, label=f"Initial $f_0={f0}$")
plt.xlabel("Temperature $T$")
plt.ylabel(r"Final Misfolded Fraction $\langle f \rangle$")
plt.title(f"Finite-Size Exploratory Scan: $\\langle f \\rangle$ vs $T$\n($J={J}, h={h}, f_0={f0}$)")
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend()
plt.tight_layout()

plot1_path = os.path.join(results_dir, "fss_mean_f_vs_T.png")
plt.savefig(plot1_path, dpi=300)
plt.close()

# ====================================================
# Plot 2: Proxy Susceptibility chi_f^(run) vs T
# ====================================================

plt.figure(figsize=(8, 6))
for idx, L in enumerate(L_values):
    sub_df = df[df["L"] == L]
    plt.plot(
        sub_df["T"], sub_df["chi_f_run"],
        "-s", color=colors[idx], label=f"L = {L}"
    )

plt.xlabel("Temperature $T$")
plt.ylabel(r"Inter-Run Proxy Susceptibility $\chi_f^{(\mathrm{run})} = \frac{N}{T} \mathrm{Var}(f)$")
plt.title(f"Finite-Size Exploratory Scan: Fluctuation Proxy $\\chi_f^{{(\\mathrm{{run}})}}$ vs $T$\n($J={J}, h={h}, f_0={f0}$)")
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend()
plt.tight_layout()

plot2_path = os.path.join(results_dir, "fss_chi_vs_T.png")
plt.savefig(plot2_path, dpi=300)
plt.close()

print("\n=== FSS Exploratory Scan Completed ===")
print(f"CSV saved to: {csv_path}")
print(f"Plot 1 saved to: {plot1_path}")
print(f"Plot 2 saved to: {plot2_path}")
