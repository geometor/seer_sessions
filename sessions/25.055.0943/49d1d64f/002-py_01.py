"""
Replicate each pixel in the 2x2 input grid into a 2x2 block in the output grid.
Then, add a white (value 0) border around the resulting 4x4 grid.
"""

import numpy as np

def replicate_pixel(grid, row, col, output_grid):
    """Replicates a single pixel into a 2x2 block."""
    value = grid[row, col]
    output_grid[2*row:2*row+2, 2*col:2*col+2] = value
    return output_grid

def transform(input_grid):
    """Transforms the input grid according to the replication and bordering rule."""
    # Initialize output_grid as a 4x4 grid filled with zeros (white).
    output_grid = np.zeros((4, 4), dtype=int)

    # Replicate each pixel of the input grid.
    for row in range(input_grid.shape[0]):
        for col in range(input_grid.shape[1]):
            output_grid = replicate_pixel(input_grid, row, col, output_grid)
            

    return output_grid