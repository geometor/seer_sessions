"""
1.  **Create Output Grid:** Create an output grid with dimensions twice the height and three times the width of the input grid.
2.  **Replicate Input:** Copy the input grid into each of six regions within the output grid. These regions are arranged in a 2x3 grid, and each region has the same dimensions as the input grid.
3.  **Cyclic Permutation (Within Each Region):** Within *each* region of the output grid, perform a cyclic permutation of the pixels as follows, where (r, c) represents the row and column indices *within the region*:
    *   The element at (0, 0) moves to (0, 1).
    *   The element at (0, 1) moves to (1, 0).
    *   The element at (0, 2) moves to (0, 0).
    *   The element at (1, 0) moves to (0, 2).
    *   The element at (1, 1) stays at (1, 1).
    *   The element at (1, 2) moves to (2, 0).
    *   The element at (2, 0) moves to (1, 2).
    *   The element at (2, 1) stays at (2, 1)
    *   The element at (2, 2) stays at (2, 2)

4.  **Iterative Application:** Apply this permutation process independently to all six regions.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape
    output_height = 2 * input_height
    output_width = 3 * input_width
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # replicate input into each region
    for i in range(2):
        for j in range(3):
            output_grid[i * input_height:(i + 1) * input_height, j * input_width:(j + 1) * input_width] = input_grid

    # cyclic permutation within each region
    for i in range(2):
        for j in range(3):
            region_view = output_grid[i * input_height:(i + 1) * input_height, j * input_width:(j + 1) * input_width]
            temp_grid = np.copy(region_view)  # Work on a copy to avoid changing during iteration

            # Apply the permutation
            region_view[0, 1] = temp_grid[0, 0]
            region_view[1, 0] = temp_grid[0, 1]
            region_view[0, 0] = temp_grid[0, 2]
            region_view[0, 2] = temp_grid[1, 0]
            # (1, 1) remains unchanged
            region_view[2, 0] = temp_grid[1, 2]
            region_view[1, 2] = temp_grid[2, 0]
            # (2, 1) and (2, 2) remain unchanged

    return output_grid