"""
1.  **Identify Influencers:** Locate all gray (5) pixels within the input grid.
2.  **Determine Affected Rows and Columns:**  Identify all rows and columns that contain at least one gray pixel.
3.  **Conditional Color Change:** A white (0) pixel in the input grid will change to red (2) in the output grid if and only if it lies in *either* a row *or* a column containing a gray pixel (identified in step 2).
4.  **Preserve Other Pixels:** All pixels that are not white, and all white pixels that do not meet the condition in step 3, remain unchanged in the output grid.
"""

import numpy as np

def get_gray_pixel_positions(grid):
    # helper to find gray pixels
    gray_pixels = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == 5:
                gray_pixels.append((r, c))
    return gray_pixels

def transform(input_grid):
    # initialize output_grid as a copy of input
    output_grid = np.copy(input_grid)

    # find gray pixels
    gray_pixels = get_gray_pixel_positions(input_grid)

    # determine rows and columns with gray
    rows_with_gray = set()
    cols_with_gray = set()
    for r, c in gray_pixels:
        rows_with_gray.add(r)
        cols_with_gray.add(c)

    # change white pixels to red if in target row or col
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if input_grid[r, c] == 0:
                if r in rows_with_gray or c in cols_with_gray:
                    output_grid[r, c] = 2

    return output_grid