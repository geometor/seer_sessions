"""
Iterates through the input grid. If a pixel's value is 0, it changes the pixel's value to 8 if the sum of the row and column indices is even, and to 1 if the sum is odd. If a pixel's value is 5, the pixel's value remains unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    output_grid = np.copy(input_grid)  # Initialize output_grid
    rows, cols = input_grid.shape

    # Iterate through each cell of the grid
    for i in range(rows):
        for j in range(cols):
            # Conditional Replacement for 0
            if input_grid[i, j] == 0:
                if (i + j) % 2 == 0:
                    output_grid[i, j] = 8  # Even sum: change to 8
                else:
                    output_grid[i, j] = 1  # Odd sum: change to 1
            elif input_grid[i,j] == 5:
                output_grid[i,j] = 5 # Value 5: no change
            # else, retain the original non-zero value, by doing nothing since we initialized with a copy

    return output_grid