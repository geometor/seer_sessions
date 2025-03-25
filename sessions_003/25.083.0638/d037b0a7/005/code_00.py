"""
The transformation rule involves propagating non-zero values from the right and bottom edges of the input grid. Vertical propagation takes precedence over horizontal propagation.  Non-zero values propagate downwards within a column until a non-zero cell is encountered. Non-zero values on the bottom row propagate to the right until a non-zero cell is encountered or if the cell has already been set by vertical propagation.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Vertical Propagation (from right to left)
    for j in range(cols - 1, -1, -1):
        for i in range(rows - 1, -1, -1):
            if output_grid[i, j] != 0:
                # Propagate downwards until a non-zero value is encountered
                for k in range(i + 1, rows):
                    if output_grid[k, j] == 0:
                        output_grid[k, j] = output_grid[i, j]
                    else:
                        break  # Stop propagation when a non-zero cell is hit

    # Bottom Row Propagation (left to right, only if not already set by vertical)
    for j in range(cols - 1):
        if output_grid[rows - 1, j] != 0:
            # Propagate to the right until a non-zero value is hit or already set
            for k in range(j + 1, cols):
                if output_grid[rows - 1, k] == 0:  # Check if already set
                    output_grid[rows - 1, k] = output_grid[rows - 1, j]
                else:
                    break

    return output_grid