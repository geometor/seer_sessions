"""
1. **Identify Reference Location:** in all the examples, The upper leftmost value of the output grid always matches with the upper leftmost non zero value of the input grid.
2. **Extract Subgrid:** Extract a 2x2 subgrid. The topleft element is the location of the reference point.
"""

import numpy as np

def find_top_left_nonzero(grid):
    """Finds the row and column indices of the top-leftmost non-zero element in a grid."""
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] != 0:
                return i, j  # Return the row and column
    return None  # Return None if no non-zero element is found

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the top-leftmost non-zero element's coordinates
    top_left_coords = find_top_left_nonzero(input_grid)

    if top_left_coords is None:
        return [[]] #return empty if no non zero is present
    start_row, start_col = top_left_coords

    # Extract the 2x2 subgrid
    output_grid = input_grid[start_row:start_row + 2, start_col:start_col + 2]

    return output_grid.tolist()