"""
Takes the '2' and '8' values from the top row and propagates them downwards 
in their respective columns, but only on every other row, starting at the 
second one (index=1). The rest of the cells are filled with zeros.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate through the first row to find source cells (2 and 8)
    for j in range(cols):
        if input_grid[0, j] == 2 or input_grid[0, j] == 8:
            source_value = input_grid[0, j]
            # Replicate the source value downward in alternating rows
            for i in range(rows):
                output_grid[0,j] = input_grid[0,j] # same as input
                if i % 2 == 1 :
                    output_grid[i, j] = source_value

    return output_grid