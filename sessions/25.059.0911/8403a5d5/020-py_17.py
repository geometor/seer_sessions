"""
1.  **Identify the Seed:** Locate the single yellow (4) pixel in the input grid.
2.  **Vertical and Horizontal Lines:** Create vertical and horizontal lines of yellow (4) pixels passing through the seed pixel, extending to the edges of the grid.
3.  **Checkerboard Fill:** Fill the remaining cells with a checkerboard pattern of 4s and 0s, starting with 0 in the cell immediately above the seed.
4.  **Corner Replacement:** Replace the values in the four corners of the grid with 5, regardless of their current value.
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

    # checkerboard fill, starting with 0 above the seed
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 0:
                if (r < seed_row and (seed_row - r) % 2 != 0) or \
                   (r > seed_row and (r - seed_row) % 2 == 0):
                    # Vertical: 0 above seed, alternate below
                    if (c < seed_col and (seed_col-c) % 2 == 0) or \
                       (c > seed_col and (c - seed_col) % 2 != 0):
                        output_grid[r,c] = 0
                    else:
                        output_grid[r,c] = 4

                elif (r < seed_row and (seed_row - r) % 2 == 0) or \
                   (r > seed_row and (r - seed_row) % 2 != 0) :
                    if (c < seed_col and (seed_col-c) % 2 == 0) or \
                       (c > seed_col and (c - seed_col) % 2 != 0):
                        output_grid[r,c] = 4
                    else:
                        output_grid[r,c] = 0
                else:
                    output_grid[r,c] = 4 # Should not reach here by design.

    # corner replacement
    output_grid[0, 0] = 5
    output_grid[0, cols-1] = 5
    output_grid[rows-1, 0] = 5
    output_grid[rows-1, cols-1] = 5

    return output_grid