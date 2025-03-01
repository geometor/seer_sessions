"""
The output image doubles the input and adds a border.
1. Border Creation: Create a new, empty grid that is twice the size of the original input grid (if input is NxN, output is 2Nx2N). 
   Copy the values of the outer edges of the input grid to create a border on the outside of the output grid.
2. Center Expansion: For each pixel *not* on the edge of the *input* grid, create a 2x2 block of pixels with the same color in the *output* grid. 
   Each of original pixel maps to a 2 x 2 square of the same color. The mapping occurs at index * 2 of the original. 
   That is, an input pixel at `(i,j)` maps to the top-left corner of its expansion at output index `(i*2, j*2)`.
"""

import numpy as np

def transform(input_grid):
    # Get the dimensions of the input grid.
    rows, cols = input_grid.shape

    # Create a new output grid that is twice the size of the input grid.
    output_grid = np.zeros((rows * 2, cols * 2), dtype=int)

    # Copy border from input
    output_grid[0, :] = np.concatenate((input_grid[0, :], input_grid[0, ::-1])) #top
    output_grid[-1, :] = np.concatenate((input_grid[-1, :], input_grid[-1, ::-1])) # bottom
    output_grid[1:-1, 0] = input_grid[1:, 0] # left, sans corners
    output_grid[1:-1, -1] = input_grid[1:, -1] # right, sans corners

    # Expand the inner pixels.
    for i in range(rows):
        for j in range(cols):
            #apply center pixel expansion rule
            output_grid[2*i, 2*j] = input_grid[i,j]
            output_grid[2*i+1, 2*j] = input_grid[i,j]
            output_grid[2*i, 2*j+1] = input_grid[i,j]
            output_grid[2*i+1, 2*j+1] = input_grid[i,j]
    return output_grid