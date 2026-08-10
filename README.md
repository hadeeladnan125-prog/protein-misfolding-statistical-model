# Physics-Based Model of Protein Misfolding Propagation

## Overview

This project develops a minimal physics-based computational model to investigate how local transitions between native and misfolded protein states can produce collective behavior at the system level.

The model uses a two-state lattice representation and Monte Carlo dynamics inspired by interacting statistical-mechanical systems.

---

## Research Question

> When can local stochastic transitions between native and misfolded protein states produce system-wide propagation, and how do interaction strength and energetic bias determine the resulting behavior?

---

## Model

Each lattice site represents a simplified protein conformational state:

* $-1 \to \text{Native}$
* $+1 \to \text{Misfolded}$

The system is described by an effective Hamiltonian:

$$H = -J \sum_{\langle i,j \rangle} s_i s_j + h \sum_i s_i$$

Where:
* **$J$**: Represents the effective interaction strength between neighboring states.
* **$h$**: Represents an energetic bias between the two states.
* **$T$**: Controls the magnitude of stochastic thermal fluctuations.

The dynamics are simulated using Metropolis Monte Carlo updates, allowing transitions in both directions:

$$\text{Native} \rightleftharpoons \text{Misfolded}$$

---

## Main Observable

The primary observable is the fraction of misfolded states over time:

$$f(t) = \frac{N_{\text{misfolded}}(t)}{N}$$

The initial stage of the project focuses on determining whether transition-like or threshold-like behavior emerges from the local interaction rules, rather than assuming that such a transition must exist.

---

## Project Structure

```text
layer1_lattice/    → Monte Carlo lattice model
layer1_meanfield/  → Mean-field approximation
notebooks/         → Analysis and visualization
results/           → Simulation outputs
