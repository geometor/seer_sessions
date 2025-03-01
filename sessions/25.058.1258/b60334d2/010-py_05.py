"""
Transforms a 9x9 grid by creating a checkerboard pattern of gray (5) and blue (1) pixels,
potentially seeded by the initial positions of gray pixels in the input. The pattern
expands as much a possible, and remaining areas are filled with white(0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rules.
    """
    output_grid = np.zeros_like(input_grid)

    # Create the 2x2 pattern element
    pattern = np.array([[5, 1], [1, 0]])

    # Determine how many times the pattern can fit completely in each dimension
    rows_fit = output_grid.shape[0] // pattern.shape[0]
    cols_fit = output_grid.shape[1] // pattern.shape[1]
    
    # Expand the pattern in blocks
    for i in range(rows_fit):
        for j in range(cols_fit):
            output_grid[i*2:(i+1)*2, j*2:(j+1)*2] = pattern

    # Special handle of the last row/column in case dimensions are not fully divisible by 2
    if output_grid.shape[0] % 2 !=0: #odd
        for j in range(cols_fit):
            output_grid[8, j*2] = 5
            output_grid[8, j*2+1] = 1
    
    if output_grid.shape[1] %2 != 0:
      if output_grid.shape[0] > 1:
        output_grid[rows_fit*2-1, cols_fit*2] = 1
        output_grid[rows_fit*2-2, cols_fit*2] = 5

    return output_grid