"""
The transformation rule is to reduce the width of the grid by half, keeping the height the same. 
The colors and their relative arrangements are preserved. Each column `i` in the output grid 
corresponds to the column `i` in the input grid.
"""

import numpy as np

def transform(input_grid):
    # Get dimensions of the input grid
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Calculate the new number of columns (half of the original)
    new_cols = cols // 2

    # Initialize the output grid with the new dimensions, filled with zeros
    output_grid = np.zeros((rows, new_cols), dtype=int)

    # Iterate through the rows and new columns
    for i in range(rows):
        for j in range(new_cols):
            # Copy the corresponding cell value from the input grid
            output_grid[i][j] = input_grid[i][j]

    return output_grid