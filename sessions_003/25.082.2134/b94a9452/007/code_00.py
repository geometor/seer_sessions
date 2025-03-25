"""
1.  **Isolate Non-Zero Region:** Identify the smallest rectangular sub-grid within the input grid that contains all non-zero pixels. This is the "isolated region".
2.  **Color Swapping:** Within the isolated region, apply the following color swaps:
    *   Swap color 2 with color 4.
    *   Swap color 1 with color 3.
    *   Swap color 4 with color 6.
3.  **Rotate:** Rotate the transformed isolated region 90 degrees clockwise. The resulting grid is the final output.
"""

import numpy as np

def _find_non_zero_region(grid):
    rows = np.any(grid != 0, axis=1)
    cols = np.any(grid != 0, axis=0)
    min_row, max_row = np.where(rows)[0][[0, -1]]
    min_col, max_col = np.where(cols)[0][[0, -1]]
    return min_row, max_row, min_col, max_col

def _swap_colors(grid):
    # Create a copy to avoid modifying the original grid
    transformed_grid = grid.copy()
    # Apply color swapping rules
    transformed_grid[grid == 2] = -1  # Temporary value for 2
    transformed_grid[grid == 4] = -2  # Temporary value for 4
    transformed_grid[grid == 1] = -3
    transformed_grid[grid == 3] = -4
    transformed_grid[grid == 6] = -5

    transformed_grid[transformed_grid == -1] = 4
    transformed_grid[transformed_grid == -2] = 6 #we swap 4 again
    transformed_grid[transformed_grid == -5] = 2 #with 6.
    transformed_grid[transformed_grid == -3] = 3
    transformed_grid[transformed_grid == -4] = 1


    return transformed_grid

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # 1. Isolate Non-Zero Region
    min_row, max_row, min_col, max_col = _find_non_zero_region(input_grid)
    isolated_region = input_grid[min_row:max_row+1, min_col:max_col+1]

    # 2. Color Swapping
    transformed_region = _swap_colors(isolated_region)

    # 3. Rotate
    rotated_region = np.rot90(transformed_region, k=-1)

    return rotated_region.tolist()