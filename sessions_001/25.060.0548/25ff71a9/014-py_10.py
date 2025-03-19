"""
The transformation rule is a simple row shift. The row containing all blue pixels (value 1) is moved from its original position (row 1, the second row which has index 1) to the bottom of the grid (row 2, which has index 2).
The row that was previously at the bottom is shifted upwards to the middle.
Essentially, the rows are rotated downwards by one position.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find the row with all blue pixels (value 1)
    blue_row_index = -1
    for i, row in enumerate(input_grid):
        if np.all(row == 1):
            blue_row_index = i
            break

    # If a blue row is found, perform the row shift
    if blue_row_index != -1:
        # Move the blue row to the bottom
        output_grid[-1, :] = input_grid[blue_row_index, :]
        #shift the other rows
        output_grid[blue_row_index: -1] = input_grid[blue_row_index + 1:]
       
    return output_grid