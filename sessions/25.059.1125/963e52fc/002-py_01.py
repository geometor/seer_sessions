"""
The input grid's horizontal band is extended by doubling it's width and adding a padding of 0 at the beginning and at the end.
"""

import numpy as np

def find_horizontal_band(grid):
    """Finds the horizontal band of non-zero values in a grid."""
    for i, row in enumerate(grid):
        non_zero_indices = np.nonzero(row)[0]
        if len(non_zero_indices) > 0:
            # Check if contiguous
            if np.all(np.diff(non_zero_indices) == 1):
                start_column = non_zero_indices[0]
                end_column = non_zero_indices[-1]
                length = end_column - start_column + 1
                row_index = i
                return start_column, end_column, length, row_index
    return None, None, None, None

def transform(input_grid):
    """Transforms the input grid by extending its horizontal band."""
    # Find the horizontal band in the input grid
    start_column, end_column, length, row_index = find_horizontal_band(input_grid)

    # if no band found, return an empty grid
    if length is None:
        return np.zeros_like(input_grid)

    # Calculate the new width
    new_width = 2 * length + 2

    # Create the extended output band
    input_band = input_grid[row_index, start_column:end_column+1]
    extended_band = np.concatenate([input_band, input_band])

    # Create output grid
    output_grid = np.zeros((input_grid.shape[0], new_width), dtype=int)

    # Populate the output grid with the extended band
    output_grid[row_index, 1:new_width-1] = extended_band
    
    return output_grid