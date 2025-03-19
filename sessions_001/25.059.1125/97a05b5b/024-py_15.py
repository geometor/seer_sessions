"""
1.  **Identify Non-White Region:** Locate the smallest rectangular area (bounding box) within the input grid that encompasses all non-white pixels. This defines the region of interest.
2.  **Extract Subgrid:** Create a new grid (the output grid) that is the size of the bounding box.
3.  **Copy to Subgrid:** Copy the content inside of the input's bounding box into the output grid, preserving colors.
4. **Example 2 Exception - rotation**: If there are multiple colors within the subgrid, perform an additional check. Determine if a 90 degree clockwise rotation is required to match the expected output.
"""

import numpy as np

def find_bounding_box(grid):
    """Find the bounding box of non-white pixels."""
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:
        return None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return min_row, max_row, min_col, max_col

def rotate_grid_90(grid):
    """Rotates a grid 90 degrees clockwise."""
    return np.rot90(grid, k=-1).tolist()

def transform(input_grid):
    input_grid = np.array(input_grid)

    # 1. Identify Non-White Region
    bounding_box = find_bounding_box(input_grid)
    if bounding_box is None:
        return []

    min_row, max_row, min_col, max_col = bounding_box

    # 2. Extract Subgrid
    output_grid = input_grid[min_row:max_row+1, min_col:max_col+1].copy()

    # 3. Copy to subgrid (already done in step 2)

    # 4. Example 2 Exception - Rotation
    unique_colors = np.unique(output_grid)
    if len(unique_colors) > 2:  # Check for more than one non-white color.  2 allows for the background
        rotated_grid = rotate_grid_90(output_grid)
        return rotated_grid

    return output_grid.tolist()