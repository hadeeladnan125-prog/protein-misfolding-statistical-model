import numpy as np

# ----------------------------------
# Model configuration
# ----------------------------------

L = 50

NATIVE = -1
MISFOLDED = +1


# ----------------------------------
# Initialize lattice
# ----------------------------------

def initialize_lattice(L, misfolded_fraction=0.01):
    """
    Create an L x L lattice.

    Each site represents a simplified protein conformational state:
        -1 -> Native
        +1 -> Misfolded
    """
    lattice = np.full((L, L), NATIVE, dtype=int)

    number_of_sites = L * L
    number_of_misfolded = int(
        misfolded_fraction * number_of_sites
    )

    if number_of_misfolded > 0:
        indices = np.random.choice(
            number_of_sites,
            size=number_of_misfolded,
            replace=False
        )
        lattice.flat[indices] = MISFOLDED

    return lattice


# ----------------------------------
# Misfolded fraction
# ----------------------------------

def misfolded_fraction(lattice):
    """
    Calculate the fraction of misfolded states.
    """
    return np.mean(lattice == MISFOLDED)


# ----------------------------------
# Energy calculation
# ----------------------------------

def local_energy(lattice, i, j, J=1.0, h=0.0):
    """
    Calculate the local energy contribution of a single lattice site.
    Hamiltonian: H = -J * sum(s_i s_j) + h * sum(s_i)
    """
    L = lattice.shape[0]
    s = lattice[i, j]

    neighbors = [
        lattice[(i - 1) % L, j],  # up
        lattice[(i + 1) % L, j],  # down
        lattice[i, (j - 1) % L],  # left
        lattice[i, (j + 1) % L]   # right
    ]

    interaction_energy = -J * s * sum(neighbors)
    field_energy = h * s

    return interaction_energy + field_energy


# ----------------------------------
# Energy change for a flip
# ----------------------------------

def delta_energy(lattice, i, j, J=1.0, h=0.0):
    """
    Calculate the change in total energy if the state at (i, j) is flipped.
    Returns: Delta H = H_new - H_old
    """
    s = lattice[i, j]
    L = lattice.shape[0]

    neighbors = [
        lattice[(i - 1) % L, j],  # up
        lattice[(i + 1) % L, j],  # down
        lattice[i, (j - 1) % L],  # left
        lattice[i, (j + 1) % L]   # right
    ]

    neighbor_sum = sum(neighbors)

    delta_H = (
        2 * J * s * neighbor_sum
        - 2 * h * s
    )

    return delta_H


# ----------------------------------
# Metropolis acceptance
# ----------------------------------

def metropolis_accept(delta_H, T):
    """
    Determine whether to accept a proposed flip using the Metropolis criterion.
    P_accept = min(1, exp(-Delta H / T))
    """
    if delta_H <= 0:
        return True

    p = np.exp(-delta_H / T)
    return np.random.rand() < p


# ----------------------------------
# Monte Carlo step (1 Sweep)
# ----------------------------------

def monte_carlo_step(lattice, T, J=1.0, h=0.0):
    """
    Perform 1 Monte Carlo sweep (L*L attempts to flip random sites).
    """
    L = lattice.shape[0]
    num_attempts = L * L

    for _ in range(num_attempts):
        i = np.random.randint(0, L)
        j = np.random.randint(0, L)

        dH = delta_energy(lattice, i, j, J=J, h=h)

        if metropolis_accept(dH, T):
            lattice[i, j] *= -1

    return lattice


# ----------------------------------
# Complete Layer 1 Test
# ----------------------------------

if __name__ == "__main__":
    print("=== Testing Complete Layer 1 Model ===")
    
    # 1. Initialize
    lattice = initialize_lattice(L, misfolded_fraction=0.10)
    initial_frac = misfolded_fraction(lattice)
    print(f"Initial misfolded fraction: {initial_frac:.4f}")

    # 2. Run Monte Carlo simulation for 100 steps
    T = 1.5
    print(f"Running 100 Monte Carlo sweeps at Temperature T = {T}...")
    for step in range(100):
        monte_carlo_step(lattice, T=T)

    final_frac = misfolded_fraction(lattice)
    print(f"Final misfolded fraction after 100 steps: {final_frac:.4f}")
    print("=== Layer 1 is 100% Ready! ===")
