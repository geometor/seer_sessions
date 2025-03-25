"""
1.  **Isolate Non-Zero Region:** Find the smallest rectangular region within the input grid that contains all the non-zero pixels. This region becomes the object of our focus.

2.  **Identify Key Colors:**
    *   Find the color value of the center pixel within the isolated region.
    *   Find the color value of a pixel directly adjacent to the isolated region in the original grid. If the isolated region extends to the edge of the input_grid so that there is no adjacent pixel, the surrounding color is considered to be 0 (black).

3.  **Swap Colors:** Within the isolated region, swap all occurrences of the center pixel's color with the surrounding pixel's color.

4.  **Rotate:** Rotate the isolated region clockwise by 90 degrees. This rotated region is the output.
"""

import numpy as np

def _find_non_zero_region(grid):
    rows = np.any(grid != 0, axis=1)
    cols = np.any(grid != 0, axis=0)
    min_row, max_row = np.where(rows)[0][[0, -1]]
    min_col, max_col = np.where(cols)[0][[0, -1]]
    return min_row, max_row, min_col, max_col

def _get_surrounding_color(grid, min_row, max_row, min_col, max_col):
    if min_row > 0:
        return grid[min_row - 1, min_col]
    elif max_row < grid.shape[0] - 1:
        return grid[max_row + 1, min_col]
    elif min_col > 0:
        return grid[min_row, min_col -1]
    elif max_col < grid.shape[1] -1:
        return grid[min_row, max_col + 1]
    return 0

def _swap_colors(grid, center_color, surround_color):
    # Create a copy to avoid modifying the original grid.
    swapped_grid = grid.copy()
    # only swap the center color with surround color
    swapped_grid[grid == center_color] = surround_color
    return swapped_grid

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # 1. Isolate Non-Zero Region
    min_row, max_row, min_col, max_col = _find_non_zero_region(input_grid)
    isolated_region = input_grid[min_row:max_row+1, min_col:max_col+1]

    # 2. Identify Key Colors
    center_row = (isolated_region.shape[0] - 1) // 2
    center_col = (isolated_region.shape[1] - 1) // 2
    center_color = isolated_region[center_row, center_col]
    surround_color = _get_surrounding_color(input_grid, min_row, max_row, min_col, max_col)

    # 3. Swap Colors
    swapped_region = _swap_colors(isolated_region, center_color, surround_color)

    # 4. Rotate
    rotated_region = np.rot90(swapped_region, k=-1)

    return rotated_region.tolist()