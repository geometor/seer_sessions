"""
Transforms a 1x5 input grid into a 10x10 output grid.  Diagonals are drawn in
the output grid for each pixel in the input grid, starting from a point on a
rising diagonal along the lower-left to upper-right corners.  The lengths of
the diagonals increase by one, from 1 to 5, using each input color.
"""

import numpy as np

def transform(input_grid):
    # Initialize a 10x10 output grid filled with zeros.
    output_grid = np.zeros((10, 10), dtype=int)
    input_height = len(input_grid)
    input_width = len(input_grid[0])
   
    # Diagonal Expansion: Iterate through each element in the input.
    for n in range(input_width):
        # Place the current input element at the bottom-left starting position.
        output_grid[10 - n -1][n] = input_grid[0][n]

        # Expand diagonally upwards and to the right, controlling the length
        for i in range(1, n + 1):  # Corrected the loop range
           if 10 - n - 1 - i >= 0 and n + i < 10:
            output_grid[10 - n - 1 - i][n + i] = input_grid[0][n]
    return output_grid