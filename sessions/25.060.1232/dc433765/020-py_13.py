"""
1. Identify the green object: Find the single green pixel (value '3') in the input grid.
2. Attempt to move right: Attempt to move the green pixel one cell to the right.
3. Boundary condition: If the green pixel is at *any* edge of the grid (leftmost, rightmost, topmost, or bottommost), do not move. If a move to the right would place the object outside the grid, do not move.
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
        #Added an else to explicitly handle case where object is on any boundary
        else:
            output_grid[row,col]=3

    return output_grid