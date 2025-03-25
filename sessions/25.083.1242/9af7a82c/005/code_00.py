"""
1.  Input: Take the input grid.
2.  Reverse Columns: Reverse the order of the columns of the input grid.
3.  Calculate Output Dimensions:
    *   The output grid's height is equal to the input grid's width plus two.
    *    Determine the number of non-zero elements in each column of the input.
    *    The width is the number of non-zero elements in the first reversed column plus the number of reversed columns minus one.
4.  Create Output Grid: Create an output grid with the calculated dimensions, initialized with all zeros.
5.  Populate Output: Place each reversed column from the input grid into the rows of the output grid, starting from the top row.
6.  Fill Remaining: The grid should already be filled with zeros
"""

import numpy as np

def count_non_zero(column):
    """Counts non-zero elements in a column."""
    return np.count_nonzero(column)

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape

    # Reverse the columns of the input grid
    reversed_columns = []
    for j in range(input_width - 1, -1, -1):
        reversed_columns.append(input_grid[:, j])

    # Calculate Output Dimensions
    output_height = input_width + 2
    first_reversed_col_non_zero = count_non_zero(reversed_columns[0])
    output_width = first_reversed_col_non_zero + len(reversed_columns) - 1
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Populate the output grid with reversed columns
    for i, col in enumerate(reversed_columns):
        non_zero_count = count_non_zero(col)
        output_grid[i, :non_zero_count] = col[col != 0]
        output_grid[i, non_zero_count:non_zero_count + len(reversed_columns)-1] = 0 # this may not be needed

    return output_grid.tolist()