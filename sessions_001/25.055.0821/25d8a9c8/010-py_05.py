"""
The transformation copies the input grid to the output grid. 
Then, it identifies the middle row of the output grid. 
Pixels in the middle row of the output grid are transformed to gray (5). 
All other pixels in the output grid remain the same as the input.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same dimensions and values as the input grid.
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape

    # Find the middle row index.
    middle_row = height // 2

    # Set all pixels in the middle row of the output grid to gray (5).
    output_grid[middle_row, :] = 5

    return output_grid