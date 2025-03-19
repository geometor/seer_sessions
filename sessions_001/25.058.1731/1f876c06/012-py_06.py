"""
1.  **Identify:** Find all non-zero pixels in the input grid.
2.  **Move:** Shift the position of each colored (non-zero) pixel diagonally. The number of positions shifted corresponds to the value of the pixel. The movement direction depends on the original column:
    *   If the pixel's original column index is greater than or equal to the row index, the pixel moves diagonally down and to the *left*.
    *   If the pixel's original column index is less that the row index, the pixel moves diagonally down and to the *right*.
3.  **Output:** Create a new grid of the same dimensions as the input. Place each shifted pixel in its new position on the output grid, retaining its original color. Pixels that would be shifted outside the grid boundaries disappear.
"""

import numpy as np

def get_nonzero_pixels(grid):
    # Find the indices of non-zero elements
    rows, cols = np.nonzero(grid)
    # Create a list of (row, col, value) tuples
    return [(r, c, grid[r, c]) for r, c in zip(rows, cols)]

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.zeros_like(input_grid)
    input_pixels = get_nonzero_pixels(input_grid)

    # Apply the shifts.
    for r, c, val in input_pixels:
      shift = val
      if c >= r:
          new_r = r + shift
          new_c = c - shift
      else:
          new_r = r + shift
          new_c = c + shift

      # Check for out-of-bounds
      if 0 <= new_r < output_grid.shape[0] and 0 <= new_c < output_grid.shape[1]:
        output_grid[new_r, new_c] = val

    return output_grid