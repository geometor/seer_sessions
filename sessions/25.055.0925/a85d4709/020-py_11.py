"""
Transforms a 3x3 grid by replacing 0 with 4 and 5 with 3.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule:
    0 -> 4
    5 -> 3
    """
    output_grid = np.copy(input_grid)  # Create a copy to avoid modifying the original

    # Iterate through each cell of the grid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Apply the substitution rules
            if output_grid[i, j] == 0:
                output_grid[i, j] = 4
            elif output_grid[i, j] == 5:
                output_grid[i, j] = 3

    return output_grid