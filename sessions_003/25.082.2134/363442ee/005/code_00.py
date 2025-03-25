"""
Replicates the object on the left side of a vertical gray line (value 5) to the right and below the line, only if the target cell is 0.
The object is also copied below both the original object and the newly copied object on the right.
"""

import numpy as np

def find_divider_column(grid):
    """Finds the column index of the vertical gray line (value 5)."""
    for j in range(grid.shape[1]):
        if np.all(grid[:, j] == 5):
            return j
    return -1

def isolate_left_object(grid, divider_column):
    """Extracts the object to the left of the divider."""
    return grid[:, :divider_column]

def transform(input_grid):
    """Transforms the input grid according to the replication rule."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    divider_col = find_divider_column(input_grid)
    left_object = isolate_left_object(input_grid, divider_col)
    left_object_height, left_object_width = left_object.shape

    # Replicate to the right
    right_start_col = divider_col + 1
    available_width_right = output_grid.shape[1] - right_start_col
    copy_width_right = min(left_object_width, available_width_right)

    for r in range(left_object_height):
        for c in range(copy_width_right):
            if right_start_col + c < output_grid.shape[1] and output_grid[r, right_start_col + c] == 0:
                output_grid[r, right_start_col + c] = left_object[r, c]

    # Replicate below original object
    bottom_start_row_left = left_object_height
    available_height_below_left = output_grid.shape[0] - bottom_start_row_left
    copy_height_below_left = min(left_object_height, available_height_below_left)
    
    for r in range(copy_height_below_left):
        for c in range(left_object_width):
           if bottom_start_row_left + r < output_grid.shape[0] and output_grid[bottom_start_row_left + r, c] == 0:
                output_grid[bottom_start_row_left + r, c] = left_object[r, c]


    # Replicate below right object
    bottom_start_row_right = left_object_height
    available_height_below_right = output_grid.shape[0] - bottom_start_row_right
    copy_height_below_right = min(left_object_height, available_height_below_right)
   

    for r in range(copy_height_below_right):
        for c in range(copy_width_right):
            if right_start_col + c < output_grid.shape[1] and bottom_start_row_right + r < output_grid.shape[0] and output_grid[bottom_start_row_right + r, right_start_col + c] == 0:

                output_grid[bottom_start_row_right + r, right_start_col + c] = left_object[r, c]

    return output_grid.tolist()