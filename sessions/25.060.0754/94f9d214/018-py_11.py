"""
The transformation identifies all green pixels in the input grid and changes their color to red. The output grid has the same dimensions as the input, and all other pixels remain white. The green pixels are replaced in place.
"""

import numpy as np

def transform(input_grid):
    # Create a copy of the input grid to serve as the output grid.
    output_grid = np.copy(input_grid)

    # Iterate through all pixels in the input grid.
    rows, cols = input_grid.shape
    for i in range(rows):
        for j in range(cols):
            # Check if the pixel is green.
            if input_grid[i, j] == 3:
                # Change the pixel color to red.
                output_grid[i, j] = 2

    return output_grid