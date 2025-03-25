"""
Transforms an input grid into an output grid where the first row is all zeros,
and subsequent rows are all zeros if their unique values are a subset of the
first row's unique values, otherwise they are all fives.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with the same dimensions as the input
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Get unique values in the first row of the input
    first_row_unique_values = set(input_grid[0])

    # Process remaining rows
    for i in range(1, rows):
        # Get unique values in the current row
        current_row_unique_values = set(input_grid[i])

        # Check if the current row's unique values are a subset of the first row's
        if current_row_unique_values.issubset(first_row_unique_values):
            # If subset, output all 0s (already initialized to 0)
            pass
        else:
            # Otherwise, output all 5s
            output_grid[i, :] = 5

    return output_grid