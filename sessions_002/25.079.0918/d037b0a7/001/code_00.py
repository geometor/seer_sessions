"""
The transformation rule involves these steps:
1. Identify Last Column: Find the rightmost column in the input grid.
2. Add a new column: Create a new, blank, column, adjacent to the last column, with same value as the last column
3. Iterate from Second Row: Start from the second row (index 1) and go through each subsequent row.
4. Fill First Column: For the cell in first column in all rows except the first, change the value to the pixel above it in the first column of the input
5. Preserve Other Pixels: Any pixel and not one of the new one described keep their value
6. Return new array
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # get dimensions
    rows, cols = output_grid.shape
    
    # add the new column, all values are same as last column
    new_col = output_grid[:, -1]
    output_grid = np.column_stack((output_grid, new_col))

    # Iterate through rows starting from the second row (index 1)
    for i in range(1, rows):
        # set first column cell to value from row above in first column
        output_grid[i, 0] = output_grid[i-1, 0]
    
    return output_grid