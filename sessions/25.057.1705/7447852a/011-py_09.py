"""
For each red pixel (2) in the input grid, place a yellow pixel (4) to its immediate right. 
If the red pixel is at the right edge of the grid, place the yellow pixel in the first column of the same row.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell is red (2)
            if output_grid[r, c] == 2:
                # If not at the right edge, place yellow to the right
                if c + 1 < cols:
                    output_grid[r, c + 1] = 4
                # If at the right edge, wrap to the beginning of the row
                else:
                    output_grid[r, 0] = 4

    return output_grid