"""
1.  **Grid Doubling:** Create an output grid that is twice the size of the input grid in both dimensions (2N x 2M).

2.  **Border:**
    *   The top border of output is created: by taking the top row of input, concatenating a reflected version of the top row of input.
    *   The bottom border of output is created: by taking the bottom row of input, concatenating a reflected version of the top row of input.
    *   The left border of output is created: taking the left column of input and placing in corresponding indices.
    *   The right border of output is created: taking the right column of input and placing in corresponding indices.

3.  **Center Expansion:** Each pixel *not* on the edge of the *input* grid is expanded into a 2x2 block of the same color in the *output* grid. An input pixel at `(i, j)` maps to the top-left corner of its expansion at output index `(i*2, j*2)`.
"""

import numpy as np

def transform(input_grid):
    # Get the dimensions of the input grid.
    rows, cols = input_grid.shape

    # Create a new output grid that is twice the size of the input grid.
    output_grid = np.zeros((rows * 2, cols * 2), dtype=int)

    # Copy and reflect top and bottom border from input
    output_grid[0, :] = np.concatenate((input_grid[0, :], input_grid[0, ::-1])) #top
    output_grid[-1, :] = np.concatenate((input_grid[-1, :], input_grid[-1, ::-1])) # bottom
    output_grid[1:-1, 0] = input_grid[1:, 0] # left, sans corners
    output_grid[1:-1, -1] = input_grid[1:, -1] # right, sans corners
    

    # Expand the inner pixels.
    for i in range(1, rows -1):
        for j in range(1, cols - 1):
            #apply center pixel expansion rule
            output_grid[2*i, 2*j] = input_grid[i,j]
            output_grid[2*i+1, 2*j] = input_grid[i,j]
            output_grid[2*i, 2*j+1] = input_grid[i,j]
            output_grid[2*i+1, 2*j+1] = input_grid[i,j]
    return output_grid