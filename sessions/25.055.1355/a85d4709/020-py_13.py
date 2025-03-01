"""
Iterate through each cell of the input grid.
If the cell's color is gray (5), change it to green (3) in the output grid.
If the cell's color is white (0), change it to yellow (4) in the output grid.
Maintain the grid's 3x3 dimensions.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same dimensions as the input grid.
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell of the input grid.
    for i in range(rows):
        for j in range(cols):
            # Apply the color transformation rules.
            if input_grid[i, j] == 5:
                output_grid[i, j] = 3
            elif input_grid[i,j] == 0:
                output_grid[i, j] = 4
            else:
                 output_grid[i,j] = input_grid[i,j] # Added to accommodate other tasks
    return output_grid