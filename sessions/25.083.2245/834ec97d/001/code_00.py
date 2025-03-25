"""
Highlights the top and left sides of non-zero values in the input by placing '4's adjacent to them, 
while preserving the original non-zero values and keeping remaining areas as '0'.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = np.zeros((rows, cols), dtype=int)

    # Iterate through each cell of the input grid
    for i in range(rows):
        for j in range(cols):
            # If the cell's value is not 0, keep original
            if input_grid[i][j] != 0:
                output_grid[i][j] = input_grid[i][j]
            # if cell's value is 0, check neighbors
            else:
                output_grid[i][j] = 0
                # check top
                if i > 0 and input_grid[i-1][j] != input_grid[i][j]:
                    output_grid[i][j] = 4

                # check left
                if j > 0 and input_grid[i][j-1] != input_grid[i][j]:
                    output_grid[i][j] = 4

    return output_grid