"""
The output grid is the same size and shape as the input grid. Every green pixel in the input grid is changed to a red pixel in the output grid. All other pixels in the input grid are copied unchanged to the output grid.
"""

import numpy as np

def transform(input_grid):
    # Create a copy of the input grid to serve as the output grid.  This
    # ensures the size and shape are the same.
    output_grid = np.copy(input_grid)

    # Iterate through all pixels in the input grid using nested loops.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Check if the current pixel is green (value 3).
            if input_grid[i][j] == 3:
                # Change the corresponding pixel in the output grid to red (value 2).
                output_grid[i][j] = 2

    return output_grid