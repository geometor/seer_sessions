"""
The input grid consists of three columns, each of a single color.
The transformation rule is a color mapping.

Based on the provided examples:
1 -> 5
2 -> 6
3 -> 4
4 -> 3
5 -> 1
6 -> 2
8 -> 9
9 -> 8
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on a color mapping rule.
    """
    # Initialize the output grid with the same dimensions as the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each cell of the output grid.
    for i in range(rows):
        for j in range(cols):
            # Apply the color mapping based on the input value.
            if input_grid[i, j] == 1:
                output_grid[i, j] = 5
            elif input_grid[i, j] == 2:
                output_grid[i, j] = 6
            elif input_grid[i, j] == 3:
                output_grid[i, j] = 4
            elif input_grid[i, j] == 4:
                output_grid[i, j] = 3
            elif input_grid[i, j] == 5:
                output_grid[i, j] = 1
            elif input_grid[i, j] == 6:
                output_grid[i, j] = 2
            elif input_grid[i, j] == 8:
                output_grid[i, j] = 9
            elif input_grid[i, j] == 9:
                output_grid[i, j] = 8
            else:
                output_grid[i,j] = input_grid[i,j] # Should never happen

    return output_grid