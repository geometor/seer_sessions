"""
1.  **Find the Seed:** Locate the single non-zero pixel (the "seed") within the input grid. Record its color and position (row, column).

2.  **Column Propagation:** Starting from the seed's column, fill every other column entirely with the seed's color.

3.  **Row Propagation:** Starting from the seed's row and moving upwards, fill every other row with the seed's color *only* in the columns that were also propagated in step 2.

4.  **Fill with Fives:** Fill cells that are at the intersection of the propagated rows and columns with the color '5'. A cell is considered an intersection if both its row and column were part of the propagation.

5.  **Fill Background:** Fill all remaining empty cells (those not containing the seed color or '5') with '0'.
"""

import numpy as np

def find_seed(grid):
    # Find the coordinates of the non-zero pixel.
    rows, cols = np.where(grid != 0)
    if len(rows) > 0:
        return rows[0], cols[0]
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    height, width = input_grid.shape

    # Find seed location
    seed_location = find_seed(input_grid)
    if seed_location is None:
      return output_grid
    seed_row, seed_col = seed_location
    seed_value = input_grid[seed_row, seed_col]

    # Column Propagation
    for c in range(seed_col, width, 2):
        output_grid[:, c] = seed_value

    # Row Propagation
    for r in range(seed_row, -1, -2):
        for c in range(width):
            if (c - seed_col) % 2 == 0:  # Check if column was propagated
                output_grid[r, c] = seed_value

    # Fill with Fives
    for r in range(seed_row, -1, -2):
        for c in range(seed_col, width, 2):
          output_grid[r,c] = 5

    return output_grid