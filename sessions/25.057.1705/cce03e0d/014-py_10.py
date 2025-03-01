"""
Replicates a 3x3 input grid into a 9x9 output grid, filling the remaining spaces with '0' (white).
The input grid is tiled in a 3x3 pattern within the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the replication and tiling rules.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros((9, 9), dtype=int)  # Initialize 9x9 output grid with zeros

    # Tile the input grid across the output grid
    for i in range(3):
        for j in range(3):
            output_grid[i*3:(i+1)*3, j*3:(j+1)*3] = input_grid

    return output_grid.tolist()