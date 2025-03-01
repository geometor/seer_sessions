"""
The transformation rule is to remove all pixels with the color white (0) from the input grid, while keeping all other pixels and their relative positions the same. The output grid has the same dimensions as the input grid, but with white pixels removed. The transformation effectively removes a "background" of white pixels, preserving the shape formed by other colors.
"""

import numpy as np

def transform(input_grid):
    # Create a copy of the input grid to serve as the output grid.
    output_grid = np.copy(input_grid)

    # Iterate through each cell of the grid.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Check if the pixel is white (0).
            if output_grid[i, j] == 0:
                # remove the pixel
                output_grid[i,j] = 0

    return output_grid