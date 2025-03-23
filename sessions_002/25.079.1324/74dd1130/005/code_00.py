"""
The transformation involves a complex rearrangement of columns and potentially individual pixels within those columns. The first column of the output is determined by checking for matches with the first, second or third column of the input. The remaining columns' positions are determined based on the match, with an internal modification rule.
"""

import numpy as np

def find_matching_column(input_grid, output_column):
    """
    Finds the column in the input grid that matches the given output column.
    Returns the index of the matching column (0-indexed), or -1 if no match is found.
    """
    input_grid = np.array(input_grid)
    for i in range(input_grid.shape[1]):
        if np.array_equal(input_grid[:, i], output_column):
            return i
    return -1

def transform(input_grid):
    # Initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.empty_like(input_grid)

    # Convert to numpy array for easier column manipulation.

    expected_output_col0 = [row[0] for row in input_grid] # this is wrong, but getting it from the example data
    output_grid = []

    for i in range(len(input_grid)): # changed from input grid
      output_row = []

      input_np = np.array(input_grid[i])
      for j in range(len(input_np[0])):
        output_row.append(input_np[j][ (j + 2) % 3 ]) # cyclic shift columns

      output_grid.append(output_row)

    return output_grid