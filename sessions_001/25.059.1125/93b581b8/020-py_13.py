"""
1.  **Identify the Core:** Locate a 2x2 block of non-zero pixels in the input grid.  Prioritize the first such block found when scanning from top-left to bottom-right.
2.  **Preserve the Core**: Copy the 2x2 core block from the input to the output grid, at the same location.
3.  **Mirror to Corners:** Copy the entire 2x2 core to each of the four corners of the output grid.
4. **Fill Remaining:** Keep all other cells in the output grid as 0 (white).
"""

import numpy as np

def find_2x2_core(grid):
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            subgrid = grid[r:r+2, c:c+2]
            if np.all(subgrid != 0):
                return (r, c)  # Return top-left coordinates
    return None

def transform(input_grid):
    # Initialize the output grid with zeros, same size as input.
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify the Core (first 2x2 non-zero block)
    core_coords = find_2x2_core(input_grid)

    if core_coords:
        core_row, core_col = core_coords

        # 2. Preserve the core
        output_grid[core_row:core_row+2, core_col:core_col+2] = input_grid[core_row:core_row+2, core_col:core_col+2]

        # 3. Mirror to Corners (copy the *entire* core)
        output_grid[0:2, 0:2] = input_grid[core_row:core_row+2, core_col:core_col+2]  # Top-left
        output_grid[0:2, cols-2:cols] = input_grid[core_row:core_row+2, core_col:core_col+2]  # Top-right
        output_grid[rows-2:rows, 0:2] = input_grid[core_row:core_row+2, core_col:core_col+2]  # Bottom-left
        output_grid[rows-2:rows, cols-2:cols] = input_grid[core_row:core_row+2, core_col:core_col+2]  # Bottom-right

    return output_grid