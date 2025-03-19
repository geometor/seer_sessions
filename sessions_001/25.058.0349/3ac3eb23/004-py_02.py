"""
The transformation identifies '2' and '8' values in the first row of the input grid.  It replicates these values in the same columns in the output grid, but only in the second row (index 1). The rest of the cells in the output are filled with zeros. The first row of the output is a copy of the input's first row.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with zeros
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Copy the first row from input to output
    output_grid[0, :] = input_grid[0, :]

    # Iterate through the first row to find source cells (2 and 8)
    for j in range(cols):
        if input_grid[0, j] == 2 or input_grid[0, j] == 8:
            source_value = input_grid[0, j]
            # Replicate the source value in the second row (index 1)
            if rows > 1: # Ensure there is a second row.
                output_grid[1, j] = source_value

    return output_grid