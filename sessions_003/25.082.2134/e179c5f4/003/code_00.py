"""
The height and width of the output_grid are the same as the input_grid.
The pattern starts with the bottom left pixel of the input being blue (1) in the bottom left of the output. The pattern created in each row seems to be influenced by the width and the position of colors in the prior row.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    height, width = input_grid.shape

    # Copy Bottom Left:
    output_grid[height - 1, 0] = 1

    # Pattern Generation (to be refined)
    for r in range(height - 1, -1, -1):
        for c in range(width):
            if r == height -1 and c == 0:
                continue

            if r == height - 1: #first row from bottom
              if c%2 == 1:
                if output_grid[r,c-1] == 1:
                  output_grid[r,c] = 8
                else:
                  output_grid[r,c] = 1
              else:
                if output_grid[r,c-1] == 1:
                  output_grid[r,c] = 8
                else:
                  output_grid[r,c] = 1
            elif c == 0: #first column
                if output_grid[r+1,c] == 1:
                  output_grid[r,c] = 8
                else:
                  output_grid[r,c] = 1
            else:
                if output_grid[r,c-1] == 1:
                  output_grid[r,c] = 8
                elif output_grid[r+1,c] == 1:
                   output_grid[r,c] = 8
                else:
                    output_grid[r,c] = 1

    return output_grid