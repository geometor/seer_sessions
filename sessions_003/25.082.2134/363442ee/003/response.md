```python
"""
Replicates the object on the left side of a vertical gray line (value 5) to the right and below the line, only if the target cell is 0.
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
            if output_grid[r, right_start_col + c] == 0:
                output_grid[r, right_start_col + c] = left_object[r, c]

    # Replicate below
    bottom_start_row = divider_col
    available_height_below = output_grid.shape[0] - bottom_start_row
    copy_height_below = min(left_object_height, available_height_below)
    
    available_width_below = output_grid.shape[1] - right_start_col
    copy_width_below = min(left_object_width, available_width_below)
   

    for r in range(copy_height_below):
        for c in range(copy_width_below):
            if output_grid[bottom_start_row + r, right_start_col + c] == 0:
                output_grid[bottom_start_row + r, right_start_col + c] = left_object[r, c]

    return output_grid.tolist()
```