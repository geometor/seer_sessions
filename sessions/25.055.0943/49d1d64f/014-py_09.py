"""
The transformation expands the input grid by duplicating each non-central pixel into a 2x2 block while preserving the central pixel. The original grid is effectively "inflated" around its center and mirrored at the edges, with color values maintained throughout.
"""

import numpy as np

def transform(input_grid):
    """Transforms a 3x3 input grid to a 5x5 output grid according to the described rules."""

    input_grid = np.array(input_grid)
    output_grid = np.zeros((5, 5), dtype=int)

    # Place central pixel
    center_value = input_grid[1, 1]
    output_grid[2, 2] = center_value

    # Iterate through input grid and expand
    for i in range(3):
        for j in range(3):
            if (i, j) != (1, 1):  # Skip central pixel
                output_grid[i*2:i*2+2, j*2:j*2+2] = input_grid[i,j]

    return output_grid