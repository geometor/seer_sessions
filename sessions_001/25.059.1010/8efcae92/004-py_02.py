"""
The transformation rule is to extract the smallest rectangular region containing all non-white pixels from the input grid and return it as the output grid. This involves finding the minimum and maximum row and column indices occupied by non-white pixels, and then slicing the input grid to extract this region.
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Find the indices of all non-white (non-zero) pixels.
    non_white_indices = np.argwhere(input_array != 0)

    # If there are no non-white pixels, return an empty grid (or handle as appropriate).
    if non_white_indices.size == 0:
        return np.array([])  # Or perhaps a 1x1 grid with a default value

    # Find the minimum and maximum row and column indices.
    min_row, min_col = np.min(non_white_indices, axis=0)
    max_row, max_col = np.max(non_white_indices, axis=0)

    # Extract the subgrid defined by these boundaries.
    output_grid = input_array[min_row:max_row+1, min_col:max_col+1]

    return output_grid