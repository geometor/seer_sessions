"""
The function identifies a contiguous region of non-zero pixels in the input grid,
reshapes them based on a pattern, and outputs a new grid containing only the reshaped object.
"""

import numpy as np

def find_object(grid):
    """Finds the bounding box of the largest contiguous non-zero region."""
    rows, cols = np.nonzero(grid)
    if len(rows) == 0:
        return None  # No object found
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)

    object_grid = grid[min_row:max_row+1, min_col:max_col+1]
    return object_grid, (min_row, min_col)


def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    input_grid = np.array(input_grid)

    # 1. Identify the Object
    object_data = find_object(input_grid)
    if object_data is None:
        return [] # Return empty grid if no object
    
    object_grid, (min_row, min_col) = object_data


    # 2. Determine output bounding box and reshape
    
    rows, cols = object_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    for r in range(rows):
        for c in range(cols):
            output_grid[c % rows, r % cols] = object_grid[r,c]

    return output_grid.tolist()