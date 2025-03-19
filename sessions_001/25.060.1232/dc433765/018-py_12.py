"""
1. Identify the green object: Find the contiguous block of pixels with the value '3' (green). In all of the examples, this consists of a single pixel.
2. Attempt to move right: Move the green object one cell to the right.
3. Boundary condition: If the green object is in the rightmost column, do not move.
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
        # Check for boundary condition (rightmost column)
        if col < input_grid.shape[1] - 1:
            # clear old location
            output_grid[row, col] = 0
            # move it one cell to the right.
            output_grid[row, col + 1] = 3

    return output_grid