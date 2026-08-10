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
# Test
# ----------------------------------

if __name__ == "__main__":
    lattice = initialize_lattice(
        L,
        misfolded_fraction=0.01
    )

       print("Lattice shape:", lattice.shape)
    print("Misfolded fraction:", misfolded_fraction(lattice))
    e_local = local_energy(lattice, 0, 0, J=1.0, h=0.0)
    print("Local energy at (0,0):", e_local)

