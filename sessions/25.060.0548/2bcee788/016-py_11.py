"""
Transforms the input grid by:
1. Changing all background pixels (value 0) to 3 (green).
2. Identifying the contiguous non-zero object (cluster of 2s and 7s).
3. Replacing all pixels of value 2 (red) with 7 (orange).
4. Expand all 7s pixels by one step right and up.
5. The output grid is the transformed background and object.
"""

import numpy as np

def find_object(grid):
    # Find the bounding box of the non-zero elements
    rows, cols = np.nonzero(grid)
    if len(rows) == 0:  # Handle empty grid
        return None, None, None, None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Initialize output_grid with 3s (green)
    output_grid = np.full(input_grid.shape, 3)

    # Find the object's bounding box
    min_row, max_row, min_col, max_col = find_object(input_grid)

    if min_row is not None:  # Proceed only if an object was found
        # Iterate through the original object and apply transformations.
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                if input_grid[r, c] == 2:
                    # replace with 7, no expansion.
                    output_grid[r,c] = 7
                elif input_grid[r, c] == 7:
                    output_grid[r, c] = 7  # keep original 7
                    if c + 1 < output_grid.shape[1]:
                        output_grid[r, c + 1] = 7  # Expand right
                    if r -1 >= 0:
                        output_grid[r - 1, c] = 7 # Expand Up.
    return output_grid