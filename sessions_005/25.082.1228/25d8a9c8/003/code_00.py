"""
Transforms an input grid into an output grid based on the following rules:
1. The first row of the output is all 5s if all values of the input first row are the same, otherwise the first row is all 0s.
2. Subsequent rows of the output grid are all 0s if their unique values are a subset of the input first row's unique values.
   If not a subset, they are all 5s.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with the same dimensions as the input
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Get unique values in the first row of the input
    first_row_unique_values = set(input_grid[0])
    first_row_all_same = all(x == input_grid[0][0] for x in input_grid[0])

    # Process first row
    if first_row_all_same:
        output_grid[0, :] = 5
    else:
        output_grid[0, :] = 0


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