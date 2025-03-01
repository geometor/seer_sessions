"""
Replace all occurrences of the digit 7 with the digit 5, preserving the grid structure and all other digit values.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid with the same dimensions as the input
    output_grid = np.copy(input_grid)

    # Iterate through each cell of the input grid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Check if the value of the cell is 7
            if output_grid[i, j] == 7:
                # change output pixels: If the value is 7, change it to 5
                output_grid[i, j] = 5

    return output_grid