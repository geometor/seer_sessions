# 11852cab • 002 • example_3 • investigate_coder

---
```python
"""
Duplicates the vertical arms of a centrally located "cross" shape within a 2D grid.
"""

import numpy as np

def find_cross_center(grid):
    """Finds the center row of the cross shape."""
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:
        return None
    center_row = (np.max(rows) + np.min(rows)) // 2
    return center_row

def get_vertical_arm(grid, center_row):
    """Extracts the vertical arm pixels from the grid."""
    rows, cols = np.where(grid != 0)
    vertical_arm_cols = []
    for col in np.unique(cols):
        pixels_in_col = grid[rows[cols == col], col]
        if len(np.unique(pixels_in_col)) > 1 or len(pixels_in_col) <=2: #check if there are different colors, and at least 3 pixels
            continue;

        arm_rows = rows[cols==col]
        
        if center_row in arm_rows: # it's a vertical arm.
             vertical_arm_cols.append(col)


    return vertical_arm_cols
            

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = input_grid.copy()
    rows, cols = input_grid.shape

    # Find the center row of the cross
    center_row = find_cross_center(input_grid)
    if center_row is None:
        return output_grid

    # Get the vertical arms
    vertical_arm_cols = get_vertical_arm(input_grid, center_row)

    # Duplicate vertical arm
    if vertical_arm_cols:
        if center_row > 0:
            for col in vertical_arm_cols:
               output_grid[center_row -1, col ] = input_grid[center_row -1, col ]
        if center_row < rows -1:

            for col in vertical_arm_cols:
               output_grid[center_row + 1, col ] = input_grid[center_row + 1, col ]

    return output_grid
```
