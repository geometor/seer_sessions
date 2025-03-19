"""
The transformation rule is to create a checkerboard pattern on a grid with the same dimensions as the input grid. The colors for the checkerboard pattern are taken from the input grid's first two rows. The color of each cell in the output grid is determined by the sum of its row and column indices. If the sum is even, the color is taken from the first row of the input grid. If the sum is odd, the color is taken from the second row of the input grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same dimensions as the input grid.
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell of the output grid.
    for i in range(rows):
        for j in range(cols):
            # If the sum of row and column indices is even, use color from the first row.
            if (i + j) % 2 == 0:
                output_grid[i, j] = input_grid[0, 0]
            # If the sum of row and column indices is odd, use color from the second row.
            else:
                output_grid[i, j] = input_grid[1, 0]

    return output_grid