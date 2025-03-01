"""
The transformation rule is as follows:
Iterate through each row of the input grid. If a row contains all identical non-zero values, keep that row unchanged in the output grid.
If any row contains a zero or more than one distinct non-zero values change all values on that row to zero.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = input_grid.copy()
    rows = input_grid.shape[0]

    # change output pixels 
    for row_index in range(rows):
        row = input_grid[row_index]
         # Find unique non-zero values in the current row
        unique_non_zero_values = np.unique(row[row != 0])
        
        # Check if the row should be all zeros.
        if len(unique_non_zero_values) != 1:
            # If there are zero or more than one unique non zero values, set the entire row to 0.
            output_grid[row_index, :] = 0

    return output_grid