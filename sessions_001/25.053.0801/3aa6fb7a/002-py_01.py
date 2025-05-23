"""
Identify all azure (8) pixels in the input grid. For each azure pixel, check if there is an adjacent azure pixel to its right. If not, place a blue (1) pixel to its immediate right. If an azure pixel has an adjacent pixel to its left (r,c-1), a blue pixel is placed directly before that left neighbor.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current pixel is azure (8)
            if input_grid[r, c] == 8:
                # Check for adjacent azure pixel to the right
                if c + 1 < cols and input_grid[r, c + 1] != 8:
                    # Add a blue (1) pixel to the right
                    output_grid[r, c + 1] = 1
                if c+1 < cols and input_grid[r,c+1] == 8 and c > 0:
                  output_grid[r,c-1] = 1

    return output_grid