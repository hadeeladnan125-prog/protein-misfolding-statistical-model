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
# Temperature Sweep Configuration
# ==================================

L = 50

# Initial fraction of misfolded states
f0 = 0.10

# Model parameters
J = 1.0
h = 0.2

# Temperature range
T_values = [
    0.5,
    1.0,
    1.5,
    2.0,
    2.2,
    2.26,
    2.4,
    2.5,
    3.0,
    3.5,
    4.0
]

# Monte Carlo parameters
sweeps = 200
num_runs = 5


# ==================================
# Run Temperature Sweep
# ==================================

print("=== Starting Temperature Sweep ===")
print(
    f"Grid: {L}x{L} | "
    f"J: {J} | "
    f"h: {h} | "
    f"Sweeps: {sweeps} | "
    f"Runs per T: {num_runs}"
)

print()


f_means = []
f_stds = []


for T in T_values:

    final_fractions = []

    for run in range(num_runs):

        # Initialize lattice
        lattice = initialize_lattice(
            L,
            misfolded_fraction=f0
        )

        # Monte Carlo evolution
        for _ in range(sweeps):

            monte_carlo_step(
                lattice,
                T=T,
                J=J,
                h=h
            )

        # Measure final misfolded fraction
        final_fractions.append(
            misfolded_fraction(lattice)
        )

    # Statistical analysis
    mean_f = np.mean(final_fractions)

    std_f = np.std(
        final_fractions,
        ddof=1
    )

    standard_error = std_f / np.sqrt(num_runs)

    f_means.append(mean_f)
    f_stds.append(standard_error)

    print(
        f"T = {T:4.2f} | "
        f"<f> = {mean_f:.4f} "
        f"+/- {standard_error:.4f}"
    )


# ==================================
# Save Results
# ==================================

results_dir = "results"

os.makedirs(
    results_dir,
    exist_ok=True
)


df = pd.DataFrame({

    "T": T_values,

    "mean_f": f_means,

    "std_f": f_stds,

    "J": [J] * len(T_values),

    "h": [h] * len(T_values),

    "L": [L] * len(T_values)

})


csv_path = os.path.join(
    results_dir,
    "T_sweep_J1.0_h0.2.csv"
)


df.to_csv(
    csv_path,
    index=False
)


# ==================================
# Plot
# ==================================

plt.figure(
    figsize=(8, 5)
)

plt.errorbar(
    T_values,
    f_means,
    yerr=f_stds,
    fmt="-o",
    capsize=5,
    label=r"$\langle f_{\mathrm{final}}\rangle$"
)


plt.axhline(
    y=f0,
    linestyle="--",
    label=fr"Initial $f_0={f0}$"
)


plt.xlabel(
    "Temperature T"
)

plt.ylabel(
    r"Final Misfolded Fraction $\langle f\rangle$"
)

plt.title(
    "Temperature Sweep: Misfolded Fraction vs T"
    "\n"
    r"$J=1.0,\ h=0.2$"
)

plt.grid(
    True,
    linestyle=":",
    alpha=0.6
)

plt.legend()

plt.tight_layout()


plot_path = os.path.join(
    results_dir,
    "T_sweep_J1.0_h0.2.png"
)


plt.savefig(
    plot_path,
    dpi=300
)

plt.show()


print()
print("=== Temperature Sweep Completed ===")
print(f"CSV saved to: {csv_path}")
print(f"Plot saved to: {plot_path}")
