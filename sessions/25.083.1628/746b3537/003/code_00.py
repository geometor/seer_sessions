"""
The transformation extracts a subset of rows from the input grid to form the output grid. The rule for inclusion is as follows: Iterate through the rows of the input grid. If a row is identical to the *immediately preceding* row, it is skipped. Otherwise (if it's the first row, or it's different from the previous row), the row is included in the output grid. The output grid maintains the original column count of the input grid. In other words, only the first row in any sequence of identical, consecutive rows from the input is copied to the output.
"""

import numpy as np

def are_rows_equal(row1, row2):
    """Helper function to compare two rows element-wise."""
    return np.array_equal(row1, row2)

def transform(input_grid):
    """
    Transforms the input grid by selecting rows that are not identical to their preceding row.
    """
    output_grid = []
    
    # Iterate through the rows of the input grid.
    for i in range(len(input_grid)):
        # If it's the first row, add it to the output.
        if i == 0:
            output_grid.append(input_grid[i])
        # Otherwise, compare the current row to the previous row.
        else:
            # If the rows are not equal, add the current row to the output.
            if not are_rows_equal(input_grid[i], input_grid[i-1]):
                output_grid.append(input_grid[i])
    
    return output_grid