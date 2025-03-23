"""
The transformation rule identifies the single non-zero digit (focus digit) in the input grid, counts its occurrences, and constructs an output grid containing only the focus digit, repeated as many times as it appeared in the input.
"""

import numpy as np

def get_focus_digit(grid):
    # Flatten the grid and find unique non-zero values
    unique_values = np.unique(grid)
    non_zero_values = unique_values[unique_values != 0]
    
    # Return focus if only one, otherwise throw error
    if len(non_zero_values) == 1:
      return non_zero_values[0]
    else:
      raise Exception("More than one non zero digit")

def transform(input_grid):
    # Identify the focus digit
    focus_digit = get_focus_digit(input_grid)

    # Count the occurrences of the focus digit
    count = np.count_nonzero(input_grid == focus_digit)

    # Construct the output grid
    output_grid = np.full((count,), focus_digit)

    return output_grid