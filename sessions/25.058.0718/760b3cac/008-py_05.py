"""
Identifies distinct azure (8) and yellow (4) regions. Modifies the azure
region by extending it to the right. If an azure pixel is not on the far
right edge, and the pixel to its right is white (0), it changes that pixel to
azure (8). The yellow region is unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through the grid
    for r in range(rows):
        for c in range(cols):
            # Focus on azure (8) pixels
            if input_grid[r, c] == 8:
                # Check if not on the right edge
                if c + 1 < cols:
                    # Check if the pixel to the right is white (0)
                    if input_grid[r, c + 1] == 0:
                        # Change the white pixel to azure (8)
                        output_grid[r, c + 1] = 8

    return output_grid