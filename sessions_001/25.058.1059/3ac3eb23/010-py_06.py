"""
The transformation rule is as follows:
1. Identify the initial yellow pixel in the input grid.
2. Replicate vertically: For every other row starting from the row immediately below the initial yellow pixel, and working to the end, place a yellow pixel in the same column as the original yellow pixel.
3. Replicate horizontally: Starting at the row below the row of the identified pixel, and working to the end, for every other row, place a yellow pixel one cell to the left of the original and one cell to the right of the original.
"""

import numpy as np

def find_initial_yellow(grid):
    # Find the coordinates of the initial yellow pixel (value 4).
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i][j] == 4:
                return (i, j)
    return None

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)
    
    # Find the initial yellow pixel.
    initial_yellow_pos = find_initial_yellow(input_grid)
    if initial_yellow_pos is None:
        return output_grid # Return original if no yellow pixel is found.

    row, col = initial_yellow_pos

    # Replicate vertically and horizontally.
    for i in range(row + 1, output_grid.shape[0]):
        if (i - row) % 2 != 0:  # every other row
            output_grid[i, col] = 4
            if col-1 >= 0: #check if col is not out of range, and fill col to the left
               output_grid[i,col-1] = 4 
            if col+1 < output_grid.shape[1]: #check if col is not out of range, and fill col to the right
                output_grid[i, col + 1] = 4

    return output_grid