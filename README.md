# Protein Misfolding Statistical Model

A physics-based computational model of protein-state propagation using lattice dynamics and Monte Carlo simulation.

---

## 2. Physical Model (Ising Lattice Framework)

Before implementation, we define the core effective minimal model representing state dynamics.

### Lattice Setup
* **Grid:** $L \times L$ 2D lattice.
* **State Space:** Each site $i$ has a state $s_i \in \{-1, +1\}$:
  * $s_i = -1$: Native (Normal protein state)
  * $s_i = +1$: Misfolded (Pathogenic state)

### Model Hamiltonian
The energy of a given configuration is defined by:

$$H = -J \sum_{\langle i,j \rangle} s_i s_j + h \sum_i s_i$$

### Parameter Definitions
* **$J$ (Cooperative Interaction Strength):**
  * $J > 0$: Fosters localized clusters. A misfolded site ($+1$) increases the energy penalty for adjacent native sites, driving cooperative propagation.
* **$h$ (Energy Bias / External Field):**
  * Controls baseline stability. A positive bias ($h > 0$) prevents spontaneous global misfolding, maintaining native state stability unless triggered.
* **$T$ (Effective Temperature / Thermal Fluctuations):**
  * Regulates stochastic fluctuations and state-transition probability during Monte Carlo steps.
---

## 3. Dynamics (Metropolis Monte Carlo Algorithm)

To simulate state transitions over time, we employ the **Metropolis Monte Carlo** update rule:

1. **State Proposal:** Select a random site $i$ and flip its state:
   $$s_i \to -s_i$$

2. **Energy Difference Calculation:** Compute the change in total Hamiltonian energy:
   $$\Delta H = H_{\text{new}} - H_{\text{old}}$$

3. **Acceptance Criterion:**
   * If $\Delta H \leq 0$: **Accept** the spin flip unconditionally (energy decreases or stays constant).
   * If $\Delta H > 0$: **Accept** the spin flip with a Boltzmann probability:
     $$P = e^{-\Delta H / (k_B T)}$$

> **Note:** For computational simplicity, we set $k_B = 1$, making $T$ a dimensionless effective temperature parameter ($P = e^{-\Delta H / T}$).
> 
