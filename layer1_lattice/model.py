import numpy as np

def initialize_lattice(L, misfolded_fraction=0.1):
    """
    s_i = -1 (Native)
    s_i = +1 (Misfolded)
    """
    N = L * L
    num_misfolded = int(N * misfolded_fraction)
    lattice = -np.ones(N, dtype=int)
    if num_misfolded > 0:
        indices = np.random.choice(N, size=num_misfolded, replace=False)
        lattice[indices] = 1
    return lattice.reshape((L, L))

def misfolded_fraction(lattice):
    """
    f = (1/N) * sum_i (1 + s_i)/2
    """
    return np.mean(lattice == 1)

def monte_carlo_step(lattice, T, J=1.0, h=0.2):
    L = lattice.shape[0]
    for _ in range(L * L):
        i = np.random.randint(0, L)
        j = np.random.randint(0, L)
        s = lattice[i, j]
        
        # Periodic Boundary Conditions
        neighbors = (
            lattice[(i+1)%L, j] +
            lattice[(i-1)%L, j] +
            lattice[i, (j+1)%L] +
            lattice[i, (j-1)%L]
        )
        
        # H = -J * s * sum(neighbors) + h * s
        # Delta H when flipping s -> -s:
        # Delta H = 2 * s * (J * sum(neighbors) - h)
        dE = 2.0 * s * (J * neighbors - h)
        
        if dE <= 0 or np.random.rand() < np.exp(-dE / T):
            lattice[i, j] = -s

    
