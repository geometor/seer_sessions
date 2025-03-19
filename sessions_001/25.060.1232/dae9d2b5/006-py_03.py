"""
Iterate through each pixel in the input grid. If the pixel's value is 4 (yellow) or 3(green), replace it with 6 (magenta). Else, leave the pixel's original color. Return the modified grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid to avoid modifying the original
    output_grid = np.copy(input_grid)
    
    # Get the height and width of the grid
    height, width = output_grid.shape

    # Iterate over each pixel in the grid using nested loops
    for i in range(height):
        for j in range(width):
            # Check if current pixel is yellow(4) or green (3)
            if output_grid[i, j] == 4 or output_grid[i,j] == 3:
                # change the pixel to magenta
                output_grid[i, j] = 6
            # else color remains the same - so do nothing

    return output_grid