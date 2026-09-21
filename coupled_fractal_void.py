"""
/simulations/coupled_fractal_void.py
The Ultimate Synthesis: Coupled Kuramoto Oscillators Living inside the Fractal Matrix.
Where Systemic Tension Φ = [H, C] bridges phase synchronization and spatial topology.
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# =====================================================================
# 1. GENERATE THE SPATIAL ENVIRONMENT (The Constraint Framework)
# =====================================================================
GRID_SIZE = 4
MAX_DEPTH = 1  # Depth 1 gives a clean 16x16 grid (256 nodes) to prevent RAM explosion

HAMILTONIAN_SEQUENCE = [
    (0,0), (0,1), (0,2), (0,3),
    (1,3), (1,2), (1,1), (1,0),
    (2,0), (2,1), (2,2), (2,3),
    (3,3), (3,2), (3,1), (3,0)
]

def generate_spatial_topology(depth, max_depth):
    """Recursively constructs our weighted spatial matrix trail."""
    if depth > max_depth:
        return np.ones((1, 1))
    sub_scale = GRID_SIZE ** (max_depth - depth)
    canvas_dim = GRID_SIZE * sub_scale
    canvas = np.zeros((canvas_dim, canvas_dim))
    
    for step, (r, c) in enumerate(HAMILTONIAN_SEQUENCE):
        sub_matrix = generate_spatial_topology(depth + 1, max_depth)
        r_start, r_end = r * sub_scale, (r + 1) * sub_scale
        c_start, c_end = c * sub_scale, (c + 1) * sub_scale
        weight = (step + 1) / len(HAMILTONIAN_SEQUENCE)
        canvas[r_start:r_end, c_start:c_end] = sub_matrix * weight
    return canvas

# Manifest the flat 2D spatial landscape
spatial_grid = generate_spatial_topology(0, MAX_DEPTH)
GRID_DIM = spatial_grid.shape[0]
N_NODES = GRID_DIM * GRID_DIM  # 16 x 16 = 256 total coupled oscillators

# =====================================================================
# 2. CONSTRUCT THE TOPOLOGY MATRIX C AND THE SPARK MATRIX H
# =====================================================================
# Flatten the 2D spatial indices into a 1D network list
np.random.seed(1337)

# The Spark Matrix (H): Diagonal intrinsic natural frequencies of each cell
intrinsic_frequencies = np.random.normal(0.0, 0.5, size=N_NODES)
H_matrix = np.diag(intrinsic_frequencies)

# Build the Spatial Spatial Coupling Matrix (A) based on grid proximity
A = np.zeros((N_NODES, N_NODES))
K_global = 4.0  # Coupling power string

for i in range(N_NODES):
    r_i, c_i = i // GRID_DIM, i % GRID_DIM
    for j in range(N_NODES):
        if i == j: continue
        r_j, c_j = j // GRID_DIM, j % GRID_DIM
        
        # Check if they are physical spatial neighbors (Up, Down, Left, Right)
        if abs(r_i - r_j) + abs(c_i - c_j) == 1:
            # The link weight is determined by the mutual spatial value of the rooms!
            # This is the "Mixtum" in action: the space dictates the communication.
            A[i, j] = (spatial_grid[r_i, c_i] + spatial_grid[r_j, c_j]) / 2.0

# Initial phase states of the living rooms
initial_phases = np.random.uniform(-np.pi, np.pi, size=N_NODES)

# =====================================================================
# 3. CORE COUPLING SYSTEM MECHANICS
# =====================================================================
def system_dynamics(t, phases):
    """Tracks how the clocks tick while pushing against spatial constraints."""
    dtheta_dt = np.zeros(N_NODES)
    
    # Calculate phase velocities driven by frequency and weighted neighbor limits
    for i in range(N_NODES):
        coupling_sum = 0.0
        for j in range(N_NODES):
            if A[i, j] > 0:
                coupling_sum += (K_global / N_NODES) * A[i, j] * np.sin(phases[j] - phases[i])
        dtheta_dt[i] = intrinsic_frequencies[i] + coupling_sum
        
    return dtheta_dt

# Run the integration across the space-time vector
T_MAX = 20.0
t_eval = np.linspace(0, T_MAX, 200)
print(f"Propagating {N_NODES} oscillators through the fractal matrix lattices...")
sol = solve_ivp(system_dynamics, [0, T_MAX], initial_phases, t_eval=t_eval)

# Compute global phase coherence (Order Parameter R) over time to track unity
order_parameter = []
for phases in sol.y.T:
    complex_phases = np.exp(1j * phases)
    r_magnitude = np.abs(np.mean(complex_phases))
    order_parameter.append(r_magnitude)

# =====================================================================
# 4. VISUALIZE THE LIVING SYNTHESIS
# =====================================================================
plt.figure(figsize=(12, 5))

# Plot 1: The Coherence Climb (Snapping into spatial order)
plt.subplot(1, 2, 1)
plt.plot(sol.t, order_parameter, color='#d9534f', linewidth=2.5)
plt.title('Global Synchronization Profile ($R(t)$)')
plt.xlabel('Simulation Time')
plt.ylabel('Coherence Order (0 = Chaos, 1 = Unity)')
plt.grid(True, linestyle=':', alpha=0.6)

# Plot 2: Final snapshot of the system phase landscape mapped back to the 2D Fractal Layout
plt.subplot(1, 2, 2)
final_phases = sol.y[:, -1].reshape((GRID_DIM, GRID_DIM))
plt.imshow(np.sin(final_phases), cmap='twilight_shifted', interpolation='nearest')
plt.colorbar(label='Sin of Local Room Phase')
plt.title('Final Phase Matrix Topology')
plt.axis('off')

fig = plt.gcf()
fig.patch.set_facecolor('#0f0f13')
for ax in fig.axes:
    ax.set_facecolor('#0f0f13')
    ax.title.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(colors='white')

output_img = 'coupled_fractal_void_proof.png'
plt.savefig(output_img, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
print(f"Synthesis complete! Unified proof tapestry saved directly to '{output_img}'.")
