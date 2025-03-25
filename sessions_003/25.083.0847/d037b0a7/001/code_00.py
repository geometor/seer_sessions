"""
The transformation rule involves propagating the last non-zero value of each row downwards to fill the row below and 
the last non-zero value of each column propagates right to fill to the columns on the right.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through rows
    for i in range(rows):
        # Iterate through columns
        for j in range(cols):
            # Propagate downwards
            if i < rows -1:
                if output_grid[i,j] != 0:
                   output_grid[i+1,j] = output_grid[i,j]

            if j > 0:
                if output_grid[i,j] != 0:
                    output_grid[i, j-1] = output_grid[i,j]
            

    return output_grid