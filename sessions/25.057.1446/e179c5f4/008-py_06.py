"""
The transformation replaces the single '1' with '8' and replaces all '0' based on a diagonal pattern of '1' and '8' based on location.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Replace '1' with '8'
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 1:
                output_grid[r, c] = 8

    # Replace '0' based on row and column indices
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 0:
                if (r + c) % 2 == 0:
                    output_grid[r, c] = 8
                else:
                    output_grid[r, c] = 1

    return output_grid