"""
1.  **Identify the Region of Interest (ROI):** Find the smallest rectangular region within the input grid that encompasses all non-blue (non-1) and non-white(non-0) pixels. This is the bounding box of all the non-blue/non-white pixels.

2.  **Extract the ROI:** Create a new grid (the output grid) with the same dimensions as the ROI.

3.  **Copy Pixels:** Copy the pixel values from the input grid's ROI to the corresponding positions in the output grid.

4.  **Ignore other Pixels:** Pixels outside the identified ROI in the input grid are ignored.
"""

import numpy as np

def get_roi_bounds(grid):
    # Find the bounding box of non-blue/white pixels
    rows, cols = grid.shape
    min_row, min_col = rows, cols
    max_row, max_col = -1, -1

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 1 and grid[r,c] != 0:
                min_row = min(min_row, r)
                min_col = min(min_col, c)
                max_row = max(max_row, r)
                max_col = max(max_col, c)

    return min_row, min_col, max_row, max_col

def transform(input_grid):
    input_grid = np.array(input_grid)

    # Get the bounds of the ROI
    min_row, min_col, max_row, max_col = get_roi_bounds(input_grid)

    # Create the output grid based on ROI dimensions
    output_grid = np.zeros((max_row - min_row + 1, max_col - min_col + 1), dtype=int)

    # Copy the ROI to the output grid
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            output_grid[r - min_row, c - min_col] = input_grid[r, c]

    return output_grid