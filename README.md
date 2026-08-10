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
