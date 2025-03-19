"""
1.  **Find the Seed:** Locate the single yellow pixel (the "seed") in the input grid.

2.  **Create Yellow Cross:** Create a yellow cross centered at the seed's location. The cross's arms extend both horizontally and vertically.

3.  **Conditional Corner Replacement:** Examine each corner of the *input* grid. If the yellow cross's arm, extending from the seed in the input, does *not* reach that specific corner's edge in the input, place a gray pixel in the corresponding corner of the *output* grid. If the cross *does* reach the edge, the output corner remains 0.
"""

import numpy as np

def find_seed(grid):
    # Find the coordinates of the yellow (4) pixel.
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value == 4:
                return (r, c)
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = output_grid.shape

    # find seed pixel
    seed_row, seed_col = find_seed(input_grid)

    # create the yellow cross
    for r in range(rows):
        output_grid[r, seed_col] = 4
    for c in range(cols):
        output_grid[seed_row, c] = 4

    # corner replacement
    if seed_row != 0 and seed_col != 0:
      output_grid[0, 0] = 5
    if seed_row != 0 and seed_col != cols -1:
      output_grid[0, cols-1] = 5
    if seed_row != rows -1 and seed_col != 0:
      output_grid[rows-1, 0] = 5
    if seed_row != rows-1 and seed_col != cols -1:
      output_grid[rows-1, cols-1] = 5

    return output_grid