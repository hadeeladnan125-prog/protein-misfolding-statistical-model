# Results & Numerical Experiments

This directory contains simulation data, generated plots, and analysis for the statistical physics model of protein misfolding.

---

## Experiment 1: Interaction Strength Sweep ($J$-Sweep)

### Configuration
- **Initial Condition ($f_0$):** 0.10
- **Temperature ($T$):** 1.5
- **Energetic Bias ($h$):** 0.0
- **Lattice Size ($L$):** 50x50
- **Number of Sweeps:** 200
- **Independent Runs per $J$:** 5
- **Range of $J$:** [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0]

### Key Observations
1. For $J < 0.6$, thermal fluctuations disrupt cooperative alignment, resulting in partial misfolding dynamics.
2. For $J \ge 1.0$, strong coupling stabilizes uniform ordering, preventing expansion of misfolded domains.

---

## Experiment 2: Temperature Sweep with Energetic Bias ($T$-Sweep)

### Configuration
- **Initial Condition ($f_0$):** 0.10
- **Interaction Strength ($J$):** 1.0
- **Energetic Bias ($h$):** 0.2
- **Lattice Size ($L$):** 50x50
- **Number of Sweeps:** 200
- **Independent Runs per $T$:** 5
- **Range of $T$:** [0.5, 1.0, 1.5, 2.0, 2.2, 2.26, 2.4, 2.5, 3.0, 3.5, 4.0]

### Observables & Uncertainty
- **Observable:** Final misfolded fraction $\langle f \rangle$.
- **Uncertainty Quantification:** Standard Error of the Mean ($SEM = \sigma / \sqrt{N}$ with $ddof=1$).

### Key Observations
With $h = 0.2$, the $s=-1$ state is energetically favored ($E_{\text{Native}} = -h < E_{\text{Misfolded}} = +h$).
1. **Low $T$ ($T \le 1.5$):** Thermal fluctuations are suppressed by $J$ and $h$, maintaining $\langle f \rangle \approx 0$.
2. **Crossover Region ($2.0 \le T \le 2.5$):** A smooth transition occurs, crossing $f_0 = 0.10$ near $T \approx 2.5$.
3. **High $T$ ($T \ge 3.0$):** Thermal noise dominates local coupling and bias, increasing misfolding toward high-entropy states.

