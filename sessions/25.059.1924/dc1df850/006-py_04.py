"""
1.  **Preservation:** Copy all non-white (red and magenta) pixels from the input grid to the output grid.
2.  **Blue Region Identification:**
    *   Identify the rightmost red pixel's column. If no red pixels exist, do not fill any area with blue.
    *   Identify the row immediately *above* the magenta pixel. If no magenta pixels exist, do not fill with blue.
3.  **Blue Filling:** If both a rightmost red pixel and a magenta pixel exist:
    *   Fill a rectangular region with blue. This region is defined by:
        *   **Top:** The top edge of the grid (row 0).
        *   **Left:** The left edge of the grid (column 0).
        *   **Right:** The column of the rightmost red pixel.
        *   **Bottom:** The row immediately above the magenta pixel.
4. **No Blue Condition:** if there isn't a magenta and a rightmost red, then exit without adding blue
"""

import numpy as np

def find_rightmost_red(grid):
    red_pixels = np.argwhere(grid == 2)
    if len(red_pixels) == 0:
        return None
    return np.max(red_pixels[:, 1])

def find_magenta_row(grid):
    magenta_pixels = np.argwhere(grid == 6)
    if len(magenta_pixels) == 0:
        return None
    return magenta_pixels[0][0]

def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find boundaries
    rightmost_red_col = find_rightmost_red(input_grid)
    magenta_row = find_magenta_row(input_grid)

    # No Blue Condition
    if rightmost_red_col is None or magenta_row is None:
        return output_grid

    # Blue Filling
    for r in range(rows):
        for c in range(cols):
            if r < magenta_row and c <= rightmost_red_col:
                if output_grid[r,c] == 0:
                    output_grid[r, c] = 1

    return output_grid