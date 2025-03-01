"""
1. Tile Input: Create a new grid by tiling the input grid 3x3.
2. Locate Blue Pixel: Find the row index of the single blue pixel (value 1)
   within the original input grid.
3. Calculate Zeroed Row Range: Multiply the blue pixel's row index by 3. This
   result is the starting row index of the section to be zeroed out.  The
   ending row index is the starting index plus 2.
4. Zero Out Rows: Set all pixel values within the calculated row range (from
   the starting index to the ending index, inclusive) in the tiled grid to 0
   (black).
"""

import numpy as np

def find_blue_pixel_row(grid):
    # Find the row index of the blue pixel (color 1).
    rows, cols = np.where(np.array(grid) == 1)
    return rows[0] if len(rows) > 0 else -1

def transform(input_grid):
    # Tile the input grid 3x3.
    tiled_grid = np.tile(np.array(input_grid), (3, 3))

    # Find the row index of the blue pixel in the input grid.
    blue_row = find_blue_pixel_row(input_grid)

    # Handle cases where no blue pixel is present.
    if blue_row == -1:
        return tiled_grid.tolist()

    # Calculate the starting and ending row indices to zero out.
    start_row = blue_row * 3
    end_row = start_row + 2

    # Zero out the calculated rows.
    tiled_grid[start_row:end_row+1, :] = 0

    return tiled_grid.tolist()