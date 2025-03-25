"""
Pixels with the values 1, 2, 3, and 8 in the input grid change color to 5(grey) in the output grid. Pixels of other color remain the same.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Get the dimensions of the grid
    rows, cols = output_grid.shape

    # Iterate through each pixel of the grid
    for i in range(rows):
        for j in range(cols):
            # Check if the pixel value is 1, 2, 3, or 8
            if output_grid[i, j] in [1, 2, 3, 8]:
                # Change the pixel value to 5
                output_grid[i, j] = 5

    return output_grid