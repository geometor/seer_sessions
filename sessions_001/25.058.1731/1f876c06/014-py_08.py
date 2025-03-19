"""
1.  **Identify:** Locate all pixels in the input grid with a non-zero value (colored pixels).
2.  **Determine Shift Direction and Amount:** For each colored pixel:
    *   The *shift amount* is equal to the pixel's *value*.
    *   The *shift direction* is diagonal:
        *   If the pixel's original column index is greater than or equal to its original row index, the shift is *down and to the left*.
        *   If the pixel's original column index is less than its original row index, the shift is *down and to the right*.
3.  **Move Pixels:** Shift each pixel by the calculated amount in the determined direction.
4.  **Boundary Check:** If a pixel's new position is outside the boundaries of the grid (row or column index is negative or greater than or equal to the grid's dimensions), the pixel disappears (its value becomes 0).
5.  **Output:** Create a new grid of the same dimensions as the input grid. Place all moved, non-disappearing pixels in their new positions on the output grid, preserving their original colors. All other cells in the output grid remain 0 (white).
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