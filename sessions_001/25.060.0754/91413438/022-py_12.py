"""
The input grid is replicated within a larger 18x18 output grid. The replication factors are determined by the dimensions of the input grid, ensuring the replicated pattern stays within the bounds of the 18x18 output. The remaining cells of the output are filled with zeros.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as an 18x18 array filled with zeros.
    output_grid = np.zeros((18, 18), dtype=int)

    # Get the dimensions of the input grid.
    input_height, input_width = input_grid.shape

    # Determine vertical and horizontal replication factors.
    vertical_replications = min(2, 18 // input_height)
    horizontal_replications = min(6, 18 // input_width)

    # Replicate the input grid.
    for i in range(vertical_replications):
        for j in range(horizontal_replications):
            output_grid[i*input_height:(i+1)*input_height, j*input_width:(j+1)*input_width] = input_grid

    return output_grid