"""
1.  **Identify Seed Pixels:** Find all pixels in the input grid that have non-zero values. These are the "seed" pixels.

2.  **Propagation with Precedence:**
    *   Each seed pixel attempts to propagate its value in two directions: *downwards* in its column and *rightwards* in its row.
    *   **Downward propagation takes precedence.**
    *   **Downward Propagation:** A seed pixel's value propagates downwards to all cells in the same column until either:
        *   It reaches the bottom of the grid.
        *   It encounters a cell that *already has a value* resulting from any other downward propagation.
    *   **Rightward Propagation:** A seed pixel's value propagates rightwards to all cells in the same row until either:
        * It reaches the right edge of the grid
        * It is blocked because the cell below that has already been filled by a downward propagation

3.  **Output:** The output grid is initialized as a copy of the input grid. The propagation rules modify the output grid, filling cells below and to the right of each seed pixel, respecting the precedence and stopping conditions. The original seed pixel values are preserved.
"""

import numpy as np

def get_nonzero_pixels(grid):
    """
    Finds the coordinates of all non-zero pixels in the grid.
    """
    rows, cols = np.where(grid != 0)
    return list(zip(rows, cols))

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # get non-zero pixels
    nonzero_pixels = get_nonzero_pixels(input_grid)

    # if no non-zero pixels, return original grid
    if not nonzero_pixels:
      return output_grid

    # Propagate downwards first (higher precedence)
    for r, c in nonzero_pixels:
        val = input_grid[r,c]
        # Propagate down
        for i in range(r + 1, height):
            if output_grid[i, c] != 0 and (i,c) not in nonzero_pixels: # Check if another downward prop already filled this cell
              break  #stop the downward prop if it hit a filled cell
            output_grid[i, c] = val

    # Propagate rightwards (lower precedence)
    for r, c in nonzero_pixels:
        val = input_grid[r, c]

        # Propagate right
        for j in range(c + 1, width):
          if output_grid[r,j] == 0:
            output_grid[r, j] = val

    return output_grid