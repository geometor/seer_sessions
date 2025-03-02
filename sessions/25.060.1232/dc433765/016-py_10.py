"""
Locate the cell containing the value '3' (green) within the input grid.
Shift the '3' one cell to the right.
Keep all other cells, including those with '0' and other non-zero values ('4' in the example) in their original positions.
"""

import numpy as np

def find_object(grid, value):
    # find the coordinates of cell with specified value
    for i, row in enumerate(grid):
        for j, cell_value in enumerate(row):
            if cell_value == value:
                return (i, j)
    return None

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # find the location of the value 3
    object_location = find_object(input_grid, 3)
    
    if object_location is not None:
        row, col = object_location
        # clear old location
        output_grid[row, col] = 0
        # move it one cell to the right.
        output_grid[row, col + 1] = 3

    return output_grid