"""
Copies non-zero pixels from a source row in the input grid to a destination row in the output grid, preserving color and relative horizontal position.  The specific source and destination rows are determined based on patterns observed across examples (currently hypothesized to be last input row and first output row, but this needs verification). Handles cases where output grid is wider than the input, padding with zeros on the left
"""

import numpy as np

def get_source_row_index(input_grid):
    """Determines the source row index in the input grid.
       Currently returns the last row. Needs adjustment based on full example analysis."""
    return input_grid.shape[0] - 1

def get_destination_row_index(output_grid):
    """Determines the destination row index in the output grid.
       Currently returns the first row. Needs adjustment based on full example analysis."""
    return 0


def transform(input_grid):
    # Determine output grid dimensions.  Assume same width as input for now, but adjust if needed.
    output_height = input_grid.shape[0] -1
    output_width = input_grid.shape[1] -1
    output_grid = np.zeros((output_height, output_width), dtype=int)


    # Determine source and destination row indices.
    source_row_index = get_source_row_index(input_grid)
    destination_row_index = get_destination_row_index(output_grid)

    # Get the source row.
    source_row = input_grid[source_row_index, :]

    # Find non-zero pixels and their indices in the source row.
    non_zero_indices = np.nonzero(source_row)[0]
    non_zero_values = source_row[non_zero_indices]

    # Calculate start index to center or left-align the copied pixels
    start_index = 0 # left align

    # Copy non-zero pixels to the destination row of the output grid.
    for i, value in enumerate(non_zero_values):
        if start_index + i < output_width:  # Check for bounds
             output_grid[destination_row_index, start_index + i] = value

    return output_grid