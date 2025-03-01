"""
1. Iterate through each cell of the input grid.
2. Check if the current cell is non-zero.
3. If the current cell is not zero, copy its color value to the cell directly below it in the output grid.
4. If a cell is zero, it remains zero in the corresponding position.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell of the input grid.
    for row in range(rows):
        for col in range(cols):
            # Check if the current cell is non-zero.
            if input_grid[row, col] != 0:
                # Copy the color value to the cell directly below,
                # but only if it's within the grid bounds.
                if row + 1 < rows:
                    output_grid[row + 1, col] = input_grid[row, col]

    return output_grid