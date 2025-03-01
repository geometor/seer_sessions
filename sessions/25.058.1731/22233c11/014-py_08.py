"""
1. Copy: Copy the input grid to the output grid.
2. Identify Object: Find the bounding box of the contiguous non-white region (the "main object") in the input grid.
3. Add Azure Pixels (Top-Left): Place two azure (8) pixels adjacent to the top-left corner of the main object's bounding box. One pixel should be directly above the top-most row of the bounding box and aligned with it's left-most column. The other should be directly to the left of the bounding box's left-most column and aligned with its top-most row.
4. Add Azure Pixels (Bottom-Right): Place two azure (8) pixels adjacent to the bottom-right corner of the main object's bounding box. One pixel should be directly below the bottom-most row of the bounding box, aligned with the bounding box's right-most column. The other pixel should be directly to the right of the right-most column, aligned with the bottom-most row of the bounding box.
5. Handle Edge Cases: If the object to be placed already exist, then no action is required.
"""

import numpy as np

def find_bounding_box(grid):
    """Finds the bounding box of the largest contiguous non-white region."""
    rows, cols = np.where(grid != 0)
    if rows.size == 0:  # Handle empty grid or all-white grid
        return None
    min_row, min_col = np.min(rows), np.min(cols)
    max_row, max_col = np.max(rows), np.max(cols)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape

    # Find bounding box of the main object
    bounding_box = find_bounding_box(input_grid)
    if bounding_box is None:
        return output_grid  # Return original if no object found

    (min_row, min_col), (max_row, max_col) = bounding_box

    # Add azure pixels to the top-left
    top_left_row1, top_left_col1 = min_row - 1, min_col
    top_left_row2, top_left_col2 = min_row, min_col - 1
    
    if 0 <= top_left_row1 < height and 0 <= top_left_col1 < width:
        if output_grid[top_left_row1, top_left_col1] != 8:
           output_grid[top_left_row1, top_left_col1] = 8
    if 0 <= top_left_row2 < height and 0 <= top_left_col2 < width:
        if output_grid[top_left_row2, top_left_col2] != 8:
            output_grid[top_left_row2, top_left_col2] = 8

    # Add azure pixels to the bottom-right
    bottom_right_row1, bottom_right_col1 = max_row + 1, max_col
    bottom_right_row2, bottom_right_col2 = max_row, max_col + 1

    if 0 <= bottom_right_row1 < height and 0 <= bottom_right_col1 < width:
        if output_grid[bottom_right_row1, bottom_right_col1] != 8:
           output_grid[bottom_right_row1, bottom_right_col1] = 8

    if 0 <= bottom_right_row2 < height and 0 <= bottom_right_col2 < width:
        if output_grid[bottom_right_row2, bottom_right_col2] != 8:
            output_grid[bottom_right_row2, bottom_right_col2] = 8


    return output_grid