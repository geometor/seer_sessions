"""
1. Identify Seeds: Find all non-zero pixels in the input grid. These are the "seed" pixels.
2. Horizontal Extension: For each seed pixel, change all pixels to its right, in the same row, to the seed pixel's color. This extends to the right edge of the grid.
3. Vertical Extension: For each seed pixel perform a vertical propogation. All pixels in the same column but lower rows are propogated to the seed pixel's color. This extension happens *after* and *includes* the horizontal extension, it starts at the right most pixel.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    for i in range(rows):
        for j in range(cols):
            if input_grid[i][j] != 0:
                # Horizontal Extension
                for k in range(j, cols):
                    output_grid[i][k] = input_grid[i][j]

                # Vertical Extension
                for r in range(i+1, rows):
                    for k in range(cols -1, j-1, -1 ):
                      if input_grid[r][j] != 0:
                          output_grid[r][k] = input_grid[r][j]


    return output_grid