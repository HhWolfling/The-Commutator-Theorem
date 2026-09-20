"""
/simulations/fractal_dungeon.py
The Corrected Spatial Manifestation of the Fractal Postulate: C = [H', C']
"""

import numpy as np
import matplotlib.pyplot as plt

GRID_SIZE = 4        
MAX_DEPTH = 2        

HAMILTONIAN_SEQUENCE = [
    (0,0), (0,1), (0,2), (0,3),
    (1,3), (1,2), (1,1), (1,0),
    (2,0), (2,1), (2,2), (2,3),
    (3,3), (3,2), (3,1), (3,0)
]

def generate_fractal_matrix(depth, max_depth):
    # Base Case: Reached atomic reality
    if depth > max_depth:
        return np.ones((1, 1))
    
    sub_scale = GRID_SIZE ** (max_depth - depth)
    canvas_dim = GRID_SIZE * sub_scale
    
    # CRITICAL MATH CHANGE: The canvas begins as open space (zeros)
    layer_canvas = np.zeros((canvas_dim, canvas_dim))
    
    for step, (r, c) in enumerate(HAMILTONIAN_SEQUENCE):
        sub_matrix = generate_fractal_matrix(depth + 1, max_depth)
        
        r_start, r_end = r * sub_scale, (r + 1) * sub_scale
        c_start, c_end = c * sub_scale, (c + 1) * sub_scale
        
        # Inject the inner complexity into the active path sequence frame
        # We scale the intensity value by the sequence index to create a path timeline
        weight = (step + 1) / len(HAMILTONIAN_SEQUENCE)
        layer_canvas[r_start:r_end, c_start:c_end] = sub_matrix * weight
        
    return layer_canvas

print(f"Igniting real structural generation down to depth {MAX_DEPTH}...")
dungeon_map = generate_fractal_matrix(depth=0, max_depth=MAX_DEPTH)

# Compute the true mathematical boundaries (the tension edges)
gy, gx = np.gradient(dungeon_map)
structural_tension = np.sqrt(gx**2 + gy**2)

# =====================================================================
# VISUALIZATION PLATFORM
# =====================================================================
plt.figure(figsize=(10, 10))

# Using 'magma' or 'inferno' to showcase the neon geometric lattice edges
plt.imshow(structural_tension, cmap='inferno', interpolation='nearest')
plt.title(f'The Infinite Dungeon: Fractal Commutator Matrix [Depth {MAX_DEPTH}]', fontsize=14, color='white')
plt.axis('off')

fig = plt.gcf()
fig.patch.set_facecolor('#0f0f13')
ax = plt.gca()
ax.set_facecolor('#0f0f13')

output_filename = 'fractal_dungeon_proof.png'
plt.savefig(output_filename, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
print(f"Void pierced! True structural layout saved straight to '{output_filename}'.")
