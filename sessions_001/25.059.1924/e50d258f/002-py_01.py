"""
1. **Identify the Bounding Box:** Scan the input grid to find the minimum and maximum row and column indices containing non-zero and non-8 (non-white and non-azure) colored pixels. This defines a rectangular bounding box within the input grid.

2. **Extract Subgrid:** Create a new, smaller grid (the output grid) with dimensions equal to the bounding box identified.

3. **Populate Output Grid:** Iterate through the cells within the bounding box of the input grid. Copy the color value of input_grid to the same related position of the output grid, only copying those pixels within the bounding box that have non-zero and non-8 colors(non-white and non-azure).

4. Return the new grid
"""

import numpy as np

def find_bounding_box(grid):
    rows, cols = grid.shape
    min_row, min_col = rows, cols
    max_row, max_col = -1, -1

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and grid[r,c] != 8:
                min_row = min(min_row, r)
                max_row = max(max_row, r)
                min_col = min(min_col, c)
                max_col = max(max_col, c)

    if min_row == rows:  # No non-zero and non-8 pixels found
       return None

    return (min_row, max_row, min_col, max_col)

def transform(input_grid):
    grid = np.array(input_grid)
    bounding_box = find_bounding_box(grid)
    
    if bounding_box is None:
        return []

    min_row, max_row, min_col, max_col = bounding_box

    # Create a new output grid based on the bounding box dimensions.
    output_grid = np.zeros((max_row - min_row + 1, max_col - min_col + 1), dtype=int)

    # Populate the output grid.
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            output_grid[r - min_row, c - min_col] = grid[r,c]

    return output_grid.tolist()