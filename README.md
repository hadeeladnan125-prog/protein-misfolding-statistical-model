# Multiscale Biophysical Dynamics of Protein Aggregation and Energetic Stress
## Abstract
**Background:** Multi-scale modeling of neurodegenerative protein misfolding often oversimplifies ionic dynamics by assuming linear Ohmic behavior. Here, we present a computational model that couples protein aggregation dynamics with non-linear ionic flux and mitochondrial ATP recovery to evaluate neuronal energetic stress ($S_E$).

**Methods:** We formulated an integrated ODE system linking aggregate kinetics to AMPAR subunit loss, dynamic calcium permeability ($P_{\text{Ca}}$), and non-linear Goldman-Hodgkin-Katz (GHK) flux. Mitochondrial ATP synthesis was incorporated through saturation kinetics. Unbound parameters were constrained using biological values. Parameter variability was tested using a Monte Carlo ensemble ($N=100$ parameter sets drawn from physiological ranges).

**Results:** Transitioning from an Ohmic approximation to GHK flux dynamics substantially reduced the estimated energetic stress $S_E(t)$ under equivalent aggregation inputs, preventing artificial over-saturation. Incorporating dynamic ATP feedback revealed that energy depletion progresses non-linearly, driven by the dynamic balance between calcium-driven ATP consumption and mitochondrial recovery capacity.

**Conclusion:** This model offers an open-source framework connecting protein aggregation to metabolic stress, providing a clearer quantitative baseline for biophysical simulations.

---

**Methods:** We formulated an integrated ODE system linking aggregate kinetics to AMPAR subunit loss, dynamic calcium permeability ($P_{\text{Ca}}$), and non-linear Goldman-Hodgkin-Katz (GHK) flux. Mitochondrial ATP synthesis was incorporated through saturation kinetics. Unbound parameters were constrained using biological values. Parameter variability was tested using a Monte Carlo ensemble ($N=100$ parameter sets drawn from physiological ranges).

**Results:** Transitioning from an Ohmic approximation to GHK flux dynamics substantially reduced the estimated energetic stress $S_E(t)$ under equivalent aggregation inputs, preventing artificial over-saturation. Incorporating dynamic ATP feedback revealed that energy depletion progresses non-linearly, driven by the dynamic balance between calcium-driven ATP consumption and mitochondrial recovery capacity.

**Conclusion:** This model offers an open-source framework connecting protein aggregation to metabolic stress, providing a clearer quantitative baseline for biophysical simulations.

---

## 1. Project Overview
This project presents a computational biophysical model linking microscopic protein aggregation to macroscopic cellular energetic stress. By integrating statistical mechanics, electrophysiology, and metabolic stoichiometric accounting, the model quantifies how aggregate-induced receptor dysregulation imposes an additional ionic pumping burden on cellular ATP reserves.

## 2. Research Question
Can microscopic protein aggregation kinetics predict macroscopic cellular energetic stress ($S_E$) via intermediate electrophysical receptor dysregulation, and how do parameter uncertainties propagate through this multiscale system?

## 3. Physical Motivation
Protein aggregation is a hallmark of neurodegenerative states, yet connecting molecular assembly to metabolic failure remains challenging. Rather than relying on purely empirical correlations, this model builds a mechanistic bridge from microscopic lattice statistics to receptor-mediated ionic flux, translating calcium overload directly into metabolic ATP demand.

## 4. Model Architecture
## 5. Mathematical Model
The multiscale framework couples three physical layers:
1. **Lattice Aggregation:** Governed by statistical-mechanical propagation yielding the aggregated fraction $f(t)$.
2. **Receptor Modulation:** Phenomenological coupling modulating GluA2-containing receptor abundance $G(t) = G_0 (1 - k_1 f(t))$.
3. **Stoichiometric Energetics:** Calcium influx via Ohmic conduction translated into ATP demand through active pump stoichiometry.

## 6. Layer 1 — Statistical Mechanics
The microscopic aggregation state $f(t) \in [0, 1]$ is derived from a mean-field lattice model describing the conformational transition and propagation kinetics of misfolded proteins.

## 7. Layer 2 — Electrophysical Coupling
The relative abundance of GluA2-containing AMPARs determines the calcium-permeable conductance $g_{\text{Ca}}(t)$:
$$g_{\text{Ca}}(t) = g_{\text{Ca},0} \cdot (1 - G(t)) = g_{\text{Ca},0} \cdot k_1 f(t)$$

The driven calcium current under constant membrane potential $V_m$ is:
$$I_{\text{Ca}}(t) = g_{\text{Ca}}(t) \cdot (V_m - E_{\text{Ca}})$$

Using Faraday's constant $F$, the excess molar calcium influx rate $\Delta\dot{n}_{\text{Ca}}$ is:
$$\Delta\dot{n}_{\text{Ca}}(t) = \frac{|I_{\text{Ca}}(t)|}{2F}$$

## 8. Layer 3 — Energetic Balance
Active clearance of excess calcium requires ATP consumption governed by the pump stoichiometry $n_{\text{ATP}}$:
$$\frac{d[\text{ATP}]}{dt} = - n_{\text{ATP}} \cdot \Delta\dot{n}_{\text{Ca}}(t)$$

The normalized Energetic Stress Index $S_E(t)$ is defined relative to the initial baseline $\text{ATP}_0$:
$$S_E(t) = 1 - \frac{\text{ATP}(t)}{\text{ATP}_0}$$

## 9. Model Classification
* **Type:** Deterministic Ordinary Differential Equation (ODE) system integrated via forward Euler / Runge-Kutta numerical schemes.
* **Domain:** Single-cell compartmental biophysics.

## 10. Dimensional Consistency
All units are explicitly defined and verified in SI / standard biophysical units:
* $I_{\text{Ca}}$ in Amperes ($\text{A}$ / $\text{pA}$)
* $\Delta\dot{n}_{\text{Ca}}$ in Moles per second ($\text{mol/s}$ / $\text{fmol/s}$)
* $[\text{ATP}]$ in Molar ($\text{M}$)
* $S_E(t)$ dimensionless ($[0, 1]$)

## 11. Control & Null Tests
Under the control state ($f(t) = 0$), the basal ATP production rate $R_{\text{prod}}$ perfectly balances baseline physiological maintenance costs. Thus, $\Delta\dot{n}_{\text{Ca}} = 0$ and $S_E(t) \equiv 0$, confirming zero artificial baseline drift.

## 12. Sensitivity Analysis
Perturbation of $k_1$ demonstrates an approximately linear scaling response of $S_E(t)$ within physiological bounds. The physical saturation threshold where $G(t) \to 0$ is defined at $k_1^{\text{sat}} \approx 11.23$.

## 13. Structural Identifiability
A critical finding of this model is a **Structural Parameter Degeneracy**. The energetic stress response depends on the multiplicative effective coupling constant:
$$K_{\text{eff}} = k_1 \cdot g_{\text{Ca},0}$$
Numerical verification confirms that distinct parameter pairs yielding identical $K_{\text{eff}}$ produce identical trajectories within double-precision machine epsilon ($\approx 2.22 \times 10^{-16}$).

## 14. Uncertainty Propagation
Parameter uncertainty in $k_1$ ($k_1 = 2.5 \pm 25\%$) was propagated using a Monte Carlo ensemble ($N = 500$, random seed = 42). The resulting spread is reported as a **95% Uncertainty Interval / Ensemble Envelope**, illustrating how parametric uncertainty expands through numerical integration over physical time.

## 15. Results
* **Baseline Trajectory:** Aggregate propagation drives steady growth in $S_E(t)$, reaching a median index of $\approx 0.12$ at $t = 5\text{ s}$.
* **Uncertainty Bounds:** The 95% ensemble envelope spans $[0.065, 0.180]$ at $t = 5\text{ s}$.

## 16. Discussion
The model describes a physics-based dynamical pathway linking molecular protein aggregation to additional energetic demand. Protein aggregation is represented by the microscopic fraction $f(t)$, obtained from the statistical-mechanical lattice model. This quantity is coupled phenomenologically to the relative abundance of GluA2-containing AMPARs, which subsequently modulates an effective calcium conductance. The resulting calcium current is converted into a molar $\text{Ca}^{2+}$ influx using Faraday's law, allowing the additional ionic load to be translated into an ATP demand through an explicit stoichiometric pumping cost.

A key feature of the model is the formulation of energetic stress relative to a balanced physiological baseline. Under the control condition, the ATP production rate compensates for basal maintenance and baseline calcium-handling costs, yielding $S_E(t)=0$. Therefore, deviations in $S_E$ under aggregation conditions represent excess energetic demand rather than an artificial baseline ATP drift.

The model predicts that increased aggregation can produce an additional energetic burden through increased $\text{Ca}^{2+}$ influx. Within the tested parameter regime, the energetic response was approximately linear with respect to the effective coupling strength. Sensitivity analysis further revealed a structural parameter degeneracy between the phenomenological coupling parameter $k_1$ and the baseline effective calcium conductance $g_{\text{Ca},0}$.

This degeneracy indicates that energetic-stress observations alone cannot independently constrain both parameters. Instead, the model output is primarily sensitive to their effective combination ($K_{\text{eff}} = k_1 \cdot g_{\text{Ca},0}$). Independent electrophysiological measurements and quantitative measurements of GluA2 abundance would therefore be required to disentangle these contributions.

## 17. Model Limitations
1. **Phenomenological Coupling:** The relation $G(t)=G_0(1-k_1f(t))$ is proposed as an effective linkage and is not directly calibrated to experimental binding kinetics.
2. **Simplified Receptor Electrophysics:** Channel conductance uses an effective Ohmic formulation rather than comprehensive biophysical modeling of AMPAR gating, desensitization, or rectification dynamics.
3. **Fixed Membrane Potential:** Membrane potential is held constant ($V_m = -70\text{ mV}$), omitting dynamic voltage feedback or action potential firing.
4. **Simplified Calcium Handling:** Calcium extrusion cost is modeled through a simplified pumping stoichiometry ($n_{\text{ATP}}$) without explicit inclusion of NCX exchangers or mitochondrial buffering systems.
5. **Constant ATP Production Rate:** Basal production rate $R_{\text{prod}}$ is kept constant to isolate the perturbation burden, omitting metabolic feedback loops or mitochondrial impairment.
6. **Parameter Identifiability:** $k_1$ and $g_{\text{Ca},0}$ are structurally unidentifiable from $S_E(t)$ measurements alone due to multiplicative coupling.
7. **No Cell-Death Claim:** The model strictly quantifies energetic stress ($S_E$) and does not claim to predict structural cell death or irreversible neurodegeneration thresholds.

## 18. Experimental Recommendations
* **To Constrain $k_1$:** Quantitative biochemical assays measuring GluA2 surface abundance as a function of measured protein aggregation fractions ($f$).
* **To Constrain $g_{\text{Ca},0}$:** Patch-clamp electrophysiology to directly measure baseline $\text{Ca}^{2+}$-permeable AMPAR current amplitudes in targeted neuronal populations.
* **To Validate Energetic Stress:** Real-time fluorometric ATP/ADP imaging under controlled ionic perturbations to calibrate $S_E(t)$ dynamics against experimental metabolic responses.

## 19. Reproducibility
All data, parameters, and generated figures are fully reproducible via the provided scripts:
* **Parameters File:** `results/parameters.json` (contains physical constants, baseline values, and random seed = 42).
* **Generated Datasets:**
  * `f_trajectory.csv`
  * `baseline_results.csv`
  * `monte_carlo_results.csv`
* **Publication Figures:**
  * `fig1_baseline_control.png` / `.pdf`
  * `fig2_monte_carlo_uncertainty.png` / `.pdf`
  * `fig3_ghk_vs_ohmic_comparison.png`
  * `fig4_final_rigorous_model.png`

## 20. Future Work
* ~~Incorporation of non-Ohmic Goldman-Hodgkin-Katz (GHK) flux equations for calcium dynamics.~~ (Completed in v2.0)
* Integration of dynamic membrane potential equations ($dV_m/dt$).
* ~~Explicit modeling of mitochondrial ATP synthesis feedback loops.~~ (Completed in v2.0)


## 21. References
1. Strikwerda, J. C. (2004). *Finite Difference Schemes and Partial Differential Equations*. SIAM.
2. Keener, J., & Sneyd, J. (2009). *Mathematical Physiology*. Springer.
3. Attwell, D., & Laughlin, S. B. (2001). An energy budget for signaling in the grey matter of the brain. *Journal of Cerebral Blood
