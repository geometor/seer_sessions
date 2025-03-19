"""
The transformation rule is as follows:
1. Identify a horizontal line of white pixels at row 3 of the input.
2. Within this row, set the left and right most pixels to blue(1). Set the rest of the values in this row to 0.
3. All Other Rows: Maintain the state of all other rows, with no changes.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    output_grid = np.copy(input_grid)  # Initialize output as a copy of the input

    # Modify Row 3 (index 2)
    row_to_modify = 2
    
    #first, set everything in the row to zero
    output_grid[row_to_modify, :] = 0
    #now, set first and last to 1
    output_grid[row_to_modify, 0] = 1
    output_grid[row_to_modify, -1] = 1


    return output_grid