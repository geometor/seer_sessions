"""
The transformation rule is as follows:
1. Copy the first two rows of the input grid to the output grid.
2. Copy the first row of the input grid to the third and fifth rows of the output grid.
3. Copy the second row of the input grid to the fourth and sixth rows of the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    # Initialize the output grid with the same dimensions as the input grid.
    output_grid = np.copy(input_grid)

    # Copy the first row to the third and fifth rows.
    output_grid[2] = input_grid[0]
    output_grid[4] = input_grid[0]

    # Copy the second row to the fourth and sixth rows.
    output_grid[3] = input_grid[1]
    output_grid[5] = input_grid[1]

    return output_grid