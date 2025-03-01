"""
1.  **Identify Red Rows:** Find all rows in the input grid that contain at least one red (2) pixel.
2.  **Extend red to full row**: extend these rows so the full row is now red, replacing previous values.
3.  **Identify Blue Columns:** Find all columns in the input grid that contain at least one blue (8) pixel.
4. **Extend blue to full column:** extend these columns so the full column is now blue, replacing previous values.
5.  **Find Intersections:** For each row identified in step 1 and each column identified in step 3, find the cell where they intersect.
6.  **Create Yellow Pixel:** At each intersection cell found in step 5, set the pixel value to yellow (4). If a pixel is part of a red row and a blue column, it always will be yellow.
7. All other pixels are unchanged.
"""

import numpy as np

def _find_rows_with_color(grid, color):
    rows = []
    for i, row in enumerate(grid):
        if color in row:
            rows.append(i)
    return rows

def _find_cols_with_color(grid, color):
    cols = []
    for j in range(grid.shape[1]):
        if color in grid[:, j]:
            cols.append(j)
    return cols

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # Find rows with red (2)
    red_rows = _find_rows_with_color(input_grid, 2)
    # Extend red rows
    for row_index in red_rows:
      output_grid[row_index, :] = 2

    # Find columns with blue (8)
    blue_cols = _find_cols_with_color(input_grid, 8)
    # Extend blue columns
    for col_index in blue_cols:
      output_grid[:, col_index] = 8

    # create yellow at intersections
    for row_index in red_rows:
        for col_index in blue_cols:
            output_grid[row_index, col_index] = 4

    return output_grid