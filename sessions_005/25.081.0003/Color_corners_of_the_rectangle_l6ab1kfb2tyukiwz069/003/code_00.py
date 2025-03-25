"""
1.  **Identify Green Rectangle:** Find the smallest and largest row and column indices that contain green (3) pixels. These define a rectangular region. This may span several rows or be within one row.

2.  **Place Orange Pixels (Top and Bottom Rows):**
    *   On the top row of the green rectangle (`min_row`):
        *   If there is a column to the left of the leftmost green pixel (`min_col > 0`), place an orange (7) pixel one position to the left.
        *    If there is a column to the right of the rightmost green pixel (`max_col < grid_width - 1`), place an orange (7) pixel one position to the right.
    * On the bottom row of the green rectangle (`max_row`):
        * If there is a column to the left of the leftmost green pixel (`min_col > 0`), place an orange (7) pixel at one position to the left .
        * If there is a column to the right of the rightmost green pixel (`max_col < grid_width -1`), place an orange (7) pixel one position to the right.

3.  **Preserve Other Pixels:** All other pixels in the output grid remain the same as in the input grid.
"""

import numpy as np

def find_green_rectangle(grid):
    # returns (min_row, max_row, min_col, max_col) of the green rectangle
    green_coords = np.argwhere(grid == 3)
    if green_coords.size > 0:
        min_row, min_col = green_coords.min(axis=0)
        max_row, max_col = green_coords.max(axis=0)
        return int(min_row), int(max_row), int(min_col), int(max_col)
    else:
        return None, None, None, None

def transform(input_grid):
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    min_row, max_row, min_col, max_col = find_green_rectangle(input_grid)

    if min_row is not None:
        # Place orange pixels on the top row
        if min_col > 0:
            output_grid[min_row, min_col - 1] = 7
        if max_col < input_grid.shape[1] - 1:
            output_grid[min_row, max_col + 1] = 7

        # Place orange pixels on the bottom row, only if distinct from the top row
        if max_row > min_row:
            if min_col > 0:
                output_grid[max_row, min_col - 1] = 7
            if max_col < input_grid.shape[1] - 1:
                output_grid[max_row, max_col + 1] = 7

    return output_grid.tolist()