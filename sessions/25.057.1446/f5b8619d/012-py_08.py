"""
1.  **Expand:** Double the dimensions of the input grid (from 6x6 to 12x12).

2.  **Replicate:** For every '5' (grey pixel) in the input grid, place a corresponding '5' in the output grid at position (row\*2, col\*2).

3.  **Create Expanded Grey Areas**:
    *   For each replicated '5', create a 2x2 block filled with a '5' using that initial '5' in the top-left position.

4.  **Frame:** Create a two-pixel wide border around the *entire output grid*, filling these border cells with '8' (azure). This is done *after* grey pixel replication.

5.  **Fill Remainder:** Fill all remaining empty cells (value 0) with '8' (azure).
"""

import numpy as np

def transform(input_grid):
    # Expand the grid
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = input_rows * 2, input_cols * 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Replicate 5s with offset and expand to 2x2
    for i in range(input_rows):
        for j in range(input_cols):
            if input_grid[i, j] == 5:
                output_grid[i * 2, j * 2] = 5
                output_grid[i * 2 + 1, j * 2] = 5
                output_grid[i * 2, j * 2 + 1] = 5
                output_grid[i * 2 + 1, j * 2 + 1] = 5

    # Frame Create (two-pixel border of 8s)
    output_grid[0:2, :] = 8
    output_grid[-2:, :] = 8
    output_grid[:, 0:2] = 8
    output_grid[:, -2:] = 8

    # Fill remainder with 8
    for i in range(output_rows):
        for j in range(output_cols):
            if output_grid[i, j] == 0:
                output_grid[i, j] = 8

    return output_grid