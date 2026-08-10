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

    Hamiltonian:
        H = -J * sum(s_i s_j) + h * sum(s_i)

    using nearest-neighbor interactions.
    """

    L = lattice.shape[0]
    s = lattice[i, j]

    # Nearest neighbors with periodic boundary conditions
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
    Calculate the change in total energy
    if the state at (i, j) is flipped.

    The proposed transition is:
        s_i -> -s_i

    Returns:
        Delta H = H_new - H_old
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
# Test
# ----------------------------------

if __name__ == "__main__":
    # Small controlled lattice
    lattice = np.array([
        [-1, -1, -1],
        [-1, +1, -1],
        [-1, -1, -1]
    ])

    J = 1.0
    h = 0.0

    print("Initial lattice:")
    print(lattice)

    i, j = 1, 1

    energy_before = local_energy(
        lattice,
        i,
        j,
        J=J,
        h=h
    )

    delta_H = delta_energy(
        lattice,
        i,
        j,
        J=J,
        h=h
    )

    print("\nState before flip:", lattice[i, j])
    print("Local energy before flip:", energy_before)
    print("Delta H:", delta_H)

    # Flip the state
    lattice[i, j] *= -1

    energy_after = local_energy(
        lattice,
        i,
        j,
        J=J,
        h=h
    )

    print("\nState after flip:", lattice[i, j])
    print("Local energy after flip:", energy_after)
