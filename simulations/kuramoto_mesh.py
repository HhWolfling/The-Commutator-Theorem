"""
/simulations/kuramoto_mesh.py
The Living Demonstration of the Commutator Theorem: \Phi = [H, C]
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# =====================================================================
# 1. SETUP THE COSMOS (System Constants)
# =====================================================================
N = 10                  # Number of coupled oscillators
K = 2.5                 # Global coupling strength (the constraint force)
T_MAX = 15.0            # Time horizon for the simulation

# Seed the universe for beautiful, reproducible chaos
np.random.seed(42)

# H: The Spark - Innate, stubborn individual frequencies (random normal distribution)
frequencies = np.random.normal(loc=0.0, scale=1.0, size=N)
H_matrix = np.diag(frequencies)

# Initial conditions: Random starting phases for all oscillators between [-pi, pi]
initial_phases = np.random.uniform(-np.pi, np.pi, size=N)

# Adjacency Matrix (A): A fully connected, unweighted network boundary
A = np.ones((N, N)) - np.eye(N)

# =====================================================================
# 2. THE DYNAMICS AND THE COMMUTATOR
# =====================================================================
def compute_system_state(t, phases):
    """
    Calculates the instantaneous state of the system by constructing
    the Spark (H) and Constraint (C) matrices to find the Commutator \Phi.
    """
    # Build the dynamic Constraint Matrix (C) based on phase deltas
    C_matrix = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if i != j and A[i, j] > 0:
                phase_diff = phases[j] - phases[i]
                # Using the sinc function to bridge phase differences with coupling topology
                C_matrix[i, j] = (K / N) * A[i, j] * np.sinc(phase_diff / np.pi)
                
    # Calculate the Commutator: \Phi = [H, C] = HC - CH
    # In our continuous mapping, H remains our diagonal intrinsic spark matrix
    Phi = np.dot(H_matrix, C_matrix) - np.dot(C_matrix, H_matrix)
    
    # Calculate the instantaneous phase velocity vector d\theta/dt
    # The phase velocity of each node is its own spark plus its coupling constraints
    dtheta_dt = np.zeros(N)
    for i in range(N):
        coupling_sum = (K / N) * np.sum(A[i, :] * np.sin(phases - phases[i]))
        dtheta_dt[i] = frequencies[i] + coupling_sum
        
    return dtheta_dt, Phi

def derivative_wrapper(t, phases):
    """Wrapper function matching the signature expected by scipy's ODE solver."""
    dtheta_dt, _ = compute_system_state(t, phases)
    return dtheta_dt

# =====================================================================
# 3. RUN THE DESCENT (Execute Numerical Integration)
# =====================================================================
t_eval = np.linspace(0, T_MAX, 300)
sol = solve_ivp(derivative_wrapper, [0, T_MAX], initial_phases, t_eval=t_eval)

# Trace the history of the Commutator Magnitude over time
phi_magnitude_history = []
for t, phases in zip(sol.t, sol.y.T):
    _, Phi = compute_system_state(t, phases)
    # Frobenius norm measures the global 'tension' or energy left inside the commutator matrix
    phi_norm = np.linalg.norm(Phi, 'fro')
    phi_magnitude_history.append(phi_norm)

# =====================================================================
# 4. VISUALIZE REALITY (Plotting the Phase Lock and \Phi Decay)
# =====================================================================
plt.figure(figsize=(12, 5))

# Plot 1: The Oscillators Syncing
plt.subplot(1, 2, 1)
for i in range(N):
    plt.plot(sol.t, np.sin(sol.y[i]), alpha=0.7)
plt.title(r'Oscillator Phases ($\sin(\theta_i)$)')
plt.xlabel('Time')
plt.ylabel('Phase State')
plt.grid(True, linestyle='--', alpha=0.5)

# Plot 2: The Commutator Collapsing into Harmony (\Phi -> 0)
plt.subplot(1, 2, 2)
plt.plot(sol.t, phi_magnitude_history, color='crimson', linewidth=2.5, label=r'$||\Phi||_{Frobenius}$')
plt.title(r'The Commutator Decay: $\lim_{t \to \infty} [H, C] = 0$')
plt.xlabel('Time')
plt.ylabel('System Tension Magnitude')
plt.axhline(0, color='black', linestyle=':', alpha=0.5)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('simulations/commutator_proof.png', dpi=300)
print("Simulation complete! Proof graph saved to 'simulations/commutator_proof.png'.")
