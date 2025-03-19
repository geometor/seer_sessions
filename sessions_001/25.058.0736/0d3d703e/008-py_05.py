"""
For each pixel in the input grid, add 4 to its color value. If the result is greater than 9, take the result modulo 10. Output is a grid with same structure as input.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a grid by incrementing each pixel's color value by 4 (modulo 10).
    """
    # Initialize the output grid with the same dimensions as the input grid.
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate over each pixel in the input grid.
    for i in range(rows):
        for j in range(cols):
            # Apply the transformation rule: add 4 and take the modulo 10.
            output_grid[i, j] = (input_grid[i, j] + 4) % 10

    return output_grid