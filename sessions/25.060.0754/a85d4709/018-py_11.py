"""
The transformation rule is a direct color substitution. Every instance of gray (color code 5) in the input grid is replaced with red (color code 2) in the output grid.  Every instance of white (color code 0) in the input grid is replaced by yellow (color code 4) in the output grid. The dimensions of the grid remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Iterate through each cell of the input grid.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Apply the color substitution rules.
            if output_grid[i, j] == 5:  # If gray
                output_grid[i, j] = 2  # Change to red
            elif output_grid[i,j] == 0: # if white
                output_grid[i,j] = 4 # Change to yellow

    return output_grid