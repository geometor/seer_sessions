"""
1. **Copy Bottom Rows:** Copy the bottom two rows (rows 4 and 5) of the input grid directly to the output grid, preserving all pixel values and positions.

2.  **Identify Center and Non Zero pixels in top rows:**
    *   Find the center cell of the entire grid (row 3, column 3).
    *   Find any non-zero pixels that are present in the top 3 rows.

3. **Add Mirrored Pixels based on top rows:** In the top three rows, for any existing non-zero pixel, add a corresponding pixel of same color in the mirrored location. For a pixel is at (r,c) a mirrored position would be also found at (r, 6-c).

4. **Fill the rest with 0:** All other cells that weren't affected are filled with 0 (white)
"""

import numpy as np

def transform(input_grid):
    output_grid = np.zeros_like(input_grid)
    h, w = output_grid.shape

    # Copy the bottom two rows
    for r in range(h-2, h):
        for c in range(w):
            output_grid[r, c] = input_grid[r, c]

    # Process top three rows, mirror around center column
    for r in range(0, h-2):
        for c in range(w):
            if input_grid[r,c] != 0:
                output_grid[r,c] = input_grid[r,c]
                output_grid[r, w - 1 - c] = input_grid[r,c]
    return output_grid