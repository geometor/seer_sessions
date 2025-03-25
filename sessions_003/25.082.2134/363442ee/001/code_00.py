"""
Replicates the object on the left side of a vertical gray line (value 5) to the right and below the line, effectively filling the space.
"""

import numpy as np

def find_divider_column(grid):
    """Finds the column index of the vertical gray line (value 5)."""
    for j in range(grid.shape[1]):
        if np.all(grid[:, j] == 5):
            return j
    return -1  # Should not happen, based on problem description

def isolate_left_object(grid, divider_column):
    """Extracts the object to the left of the divider."""
    return grid[:, :divider_column]

def transform(input_grid):
    """Transforms the input grid according to the replication rule."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    divider_col = find_divider_column(input_grid)
    left_object = isolate_left_object(input_grid, divider_col)

    # Replicate to the right
    right_start_col = divider_col + 1
    right_end_col = right_start_col + left_object.shape[1]
    
    if right_end_col > output_grid.shape[1]:
        right_end_col = output_grid.shape[1]

    output_grid[:left_object.shape[0], right_start_col:right_end_col] = left_object[:, :right_end_col - right_start_col]

    # Replicate below
    bottom_start_row = divider_col
    bottom_end_row = bottom_start_row + left_object.shape[0]
        
    if bottom_end_row > output_grid.shape[0]:
        bottom_end_row = output_grid.shape[0]

    output_grid[bottom_start_row:bottom_end_row, right_start_col:right_start_col+left_object.shape[1]] = left_object[:bottom_end_row - bottom_start_row,:]


    return output_grid.tolist()