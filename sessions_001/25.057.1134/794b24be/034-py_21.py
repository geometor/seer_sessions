"""
Iterate through every pixel of the input grid.
Check the color of input pixel.
If the color is blue (1), change it to red (2) in the output grid.
Otherwise, the output pixel color should remain unchanged from the input pixel color.
Return the modified grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Get the dimensions of the grid
    rows, cols = output_grid.shape

    # Iterate through each pixel in the grid
    for i in range(rows):
        for j in range(cols):
            # Check the color of the input pixel
            # If the color is blue (1), change it to red (2)
            if input_grid[i, j] == 1:
                output_grid[i, j] = 2
            # Otherwise, the output pixel color remains the same
            # (no explicit action needed as output_grid is initialized as a copy)

    return output_grid