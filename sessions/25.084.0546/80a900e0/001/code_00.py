"""
Copies any color that is not blue (1) or white (0) in the top-left diagonal direction within the checkerboard pattern of 1s and 0s.
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
                # Propagate Insertion Color to the left and up diagonally
                for i in range(1, min(r, c) + 1):
                    if (r - i) >= 0 and (c - i) >= 0:
                      output_grid[r-i,c-i] = current_color
    return output_grid