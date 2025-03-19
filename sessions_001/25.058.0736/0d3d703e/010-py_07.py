"""
For every pixel in the input grid, add 4 to its color value.  If the resulting value is greater than 9, take the modulo 10 of the result.  Place the new value in the corresponding pixel of the output grid. The output grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same dimensions as the input grid.
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate over each pixel in the input grid.
    for i in range(rows):
        for j in range(cols):
            # Apply the transformation rule: add 4 and take the modulo 10.
            output_grid[i, j] = (input_grid[i, j] + 4) % 10

    return output_grid