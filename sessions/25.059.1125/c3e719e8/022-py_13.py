"""
The input grid is replicated four times in a 2x2 matrix arrangement. The spacing between the replicas is dynamically calculated based on the input and output grid dimensions. The output grid dimensions are calculated using the formulas: output_height = 2 * input_height + row_gap, and output_width = 2 * input_width + col_gap, where row_gap = (output_rows - 2 * input_rows) + 1 and col_gap = (output_cols - 2 * input_cols) + 1. The remaining space in the output grid is filled with white (0).
"""

import numpy as np

def transform(input_grid, output_grid):  # Added output_grid as an argument
    # Get input grid dimensions
    input_height, input_width = input_grid.shape
    output_height, output_width = output_grid.shape

    # Calculate row and column gaps
    row_gap = (output_height - 2 * input_height) + 1
    col_gap = (output_width - 2 * input_width) + 1

    # Initialize output_grid with zeros (white) - This is now done outside, and passed.
    # output_grid = np.zeros((output_height, output_width), dtype=int)

    # Replicate and place the input grid in a 2x2 pattern
    for i in range(2):
        for j in range(2):
            # Calculate the starting row and column for each replica
            start_row = i * (input_height + row_gap)
            start_col = j * (input_width + col_gap)

            # Place the replica into the output grid
            output_grid[start_row:start_row + input_height, start_col:start_col + input_width] = input_grid

    return output_grid