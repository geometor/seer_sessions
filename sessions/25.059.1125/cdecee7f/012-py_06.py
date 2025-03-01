"""
1.  **Identify Non-Zero Region:** Examine the input grid and determine the smallest bounding rectangle that contains all non-zero pixels.
2. **Copy:** Create an output grid with the same dimensions as the bounding region.
3. **Transfer Pixels:** Transfer pixels from the input grid's bounding region to the output grid. Copy pixel values to identical output locations.
"""

import numpy as np

def find_bounding_box(grid):
    # Find rows and columns with non-zero elements
    rows = np.any(grid != 0, axis=1)
    cols = np.any(grid != 0, axis=0)

    # Get the indices of the first and last True values
    min_row, max_row = np.where(rows)[0][[0, -1]] if np.any(rows) else (0, 0)
    min_col, max_col = np.where(cols)[0][[0, -1]] if np.any(cols) else (0, 0)

    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Find the bounding box of non-zero pixels
    min_row, max_row, min_col, max_col = find_bounding_box(input_grid)

    # Create the output grid based on the bounding box dimensions
    output_grid = np.zeros((max_row - min_row + 1, max_col - min_col + 1), dtype=int)

    # Transfer pixels from the bounding region to the output grid
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            output_grid[r - min_row, c - min_col] = input_grid[r, c]

    return output_grid