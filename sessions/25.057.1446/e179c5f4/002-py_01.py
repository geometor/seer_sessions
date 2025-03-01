"""
Replaces '0' pixels in the input grid with an alternating pattern of '8' and '1' based on the sum of their row and column indices.  Pixels with values other than '0' are copied to the output grid unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    output_grid = np.copy(input_grid)  # Initialize output_grid as a copy of input_grid
    rows, cols = input_grid.shape

    # Iterate through each cell of the grid
    for i in range(rows):
        for j in range(cols):
            # Conditional Replacement
            if input_grid[i, j] == 0:
                if (i + j) % 2 == 0:
                    output_grid[i, j] = 8  # Replace with '8' if sum of row and column indices is even
                else:
                    output_grid[i, j] = 1  # Replace with '1' if sum of row and column indices is odd
            # else, retain the original non-zero value, by doing nothing since we initialized with a copy

    return output_grid