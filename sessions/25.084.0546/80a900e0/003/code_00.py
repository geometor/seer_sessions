"""
Copies any color that is not blue (1) or white (0) in the down-right diagonal direction, skipping one cell, within the checkerboard pattern of 1s and 0s.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through the input grid
    for r in range(rows):
        for c in range(cols):
            # Identify Insertion Colors: Find cells that are not blue (1) or white (0).
            if input_grid[r, c] != 1 and input_grid[r, c] != 0:
                current_color = input_grid[r, c]
                # Propagate Insertion Color to the right and down diagonally, skipping one cell
                i = 2
                while (r + i) < rows and (c + i) < cols:
                    output_grid[r + i, c + i] = current_color
                    i += 2
    return output_grid