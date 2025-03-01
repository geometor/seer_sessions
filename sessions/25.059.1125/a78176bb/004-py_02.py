"""
Keep the existing top-left to bottom-right orange diagonal, remove the 2x2 grey/orange block, and add a new orange diagonal from top-right to bottom-left.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Remove non-diagonal elements (specifically the 2x2 block)
    for i in range(rows):
        for j in range(cols):
            if i != j and output_grid[i, j] != 0:
                output_grid[i,j] = 0

    # Add the top-right to bottom-left diagonal
    for i in range(rows):
        for j in range(cols):
          if i + j == rows -1:
            output_grid[i,j] = 7

    return output_grid