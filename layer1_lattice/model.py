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
# Test
# ----------------------------------

if __name__ == "__main__":
    lattice = initialize_lattice(
        L,
        misfolded_fraction=0.01
    )

    print("Lattice shape:", lattice.shape)
    print("Misfolded fraction:", misfolded_fraction(lattice))
  
