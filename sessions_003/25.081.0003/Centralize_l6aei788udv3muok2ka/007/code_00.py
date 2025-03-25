"""
1.  **Identify the Object:** Find the smallest rectangular region within the input grid that contains all non-zero pixels. This is the object.
2.  **Find Original Center:** Calculate the center coordinates (row, column) of this rectangular object *before* rotation.
3.  **Rotate:** Rotate the object 90 degrees clockwise. This swaps the object's width and height.
4.  **Center Rotated Object:** Calculate the new center of rotated object. Place the rotated object onto a new, all-zero grid (same dimensions as input) such that the center of the rotated object is at the *same* coordinates as the center of the original object.
5. **Output**: return the modified grid
"""

import numpy as np

def find_object(grid):
    # Find coordinates of non-zero pixels
    rows, cols = np.nonzero(grid)
    if len(rows) == 0:  # Handle empty object case
        return None, None, None, None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return min_row, max_row, min_col, max_col

def rotate_object(grid, min_row, max_row, min_col, max_col):
    # Extract the object
    object_block = grid[min_row:max_row+1, min_col:max_col+1]
    # Rotate 90 degrees clockwise using numpy
    rotated_block = np.rot90(object_block, k=-1)
    return rotated_block

def transform(input_grid):
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # 1. Identify the Object
    min_row, max_row, min_col, max_col = find_object(input_grid)

    if min_row is None:  # Handle case where no object is found
        return output_grid.tolist()

    # 2. Find Original Center
    original_center_row = (min_row + max_row) // 2
    original_center_col = (min_col + max_col) // 2

    # 3. Rotate
    rotated_block = rotate_object(input_grid, min_row, max_row, min_col, max_col)
    rotated_height, rotated_width = rotated_block.shape

    # 4. Center Rotated Object
    # Calculate top-left corner of rotated object for placement
    start_row = original_center_row - rotated_height // 2
    start_col = original_center_col - rotated_width // 2

    # Ensure the rotated object stays within bounds
    start_row = max(0, min(start_row, output_grid.shape[0] - rotated_height))
    start_col = max(0, min(start_col, output_grid.shape[1] - rotated_width))

    # Place rotated block
    output_grid[start_row:start_row + rotated_height, start_col:start_col + rotated_width] = rotated_block

    return output_grid.tolist()