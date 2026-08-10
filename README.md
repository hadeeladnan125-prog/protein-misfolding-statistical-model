# Experiment Results: J Parameter Sweep

## Baseline Parameters
- **Initial Condition ($f_0$):** 0.1
- **Temperature ($T$):** 1.5
- **Lattice Size ($L$):** 50x50
- **External Field ($h$):** 0.0
- **Number of Sweeps:** 200
- **Independent Runs per J:** 5
- **Range of $J$:** [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0]

## Observables
- **$\langle f \rangle$ (mean_f):** Ensemble average of final misfolded fraction.
- **Uncertainty (std_f):** Standard error of the mean across independent realizations.

## Scientific Note
The observed behavior shows a sharp change in $\langle f \rangle$ near $J \approx 0.6$. 
This behavior represents a **transition-like / crossover phenomenon** in a finite system ($L=50$), and does NOT constitute a thermodynamic proof of a critical phase transition without finite-size scaling ($L \to \infty$) and fluctuation analysis ($\chi$).
