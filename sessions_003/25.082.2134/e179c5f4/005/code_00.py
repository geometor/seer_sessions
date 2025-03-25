"""
1.  **Initialization:** Create an output grid of the same dimensions as the input grid, filled initially with zeros.
2.  **Bottom-Left Start:** Set the bottom-left pixel of the output grid to blue (1).
3.  **Iterative Pattern Filling:** Iterate through the output grid row by row, from bottom to top (rows) and left to right (columns):
    *   If it is the bottom-left pixel, skip (already set).

    *   If in the first row from the bottom: place alternating 8 and 1.

    *  Otherwise:
        * Examine a 2x2 sub-grid that ends with the pixel being filled.
        * If all other pixels are the same, place the opposite color.
        * If mixed, then place 8.

4. **Return:** Return the filled output grid.
"""

import numpy as np

def get_2x2_subgrid(grid, row, col):
    """Helper function to get the values of the 2x2 subgrid."""
    height, width = grid.shape
    if row >= height or col >= width or row < 1 or col < 1 :
        return None  # Not a valid 2x2 subgrid

    return [
        grid[row-1, col-1],  # Top-left
        grid[row-1, col],    # Top-right
        grid[row, col-1]   # Bottom-left
           ]


def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    height, width = input_grid.shape

    # Bottom-Left Start
    output_grid[height - 1, 0] = 1

    # Iterative Pattern Filling
    for r in range(height - 1, -1, -1):
        for c in range(width):
            # Skip bottom-left
            if r == height - 1 and c == 0:
                continue

            if r == height - 1: #first row from bottom
              if c%2 == 1:
                output_grid[r,c] = 8
              else:
                output_grid[r,c] = 1
            else:
                subgrid_values = get_2x2_subgrid(output_grid, r, c)
                if subgrid_values:
                  if all(x == subgrid_values[0] for x in subgrid_values):
                      output_grid[r,c] = 8 if subgrid_values[0] == 1 else 1
                  else:
                      output_grid[r,c] = 8

                else:
                  if output_grid[r+1,c] == 1:
                      output_grid[r,c] = 8
                  else:
                      output_grid[r,c] = 1


    return output_grid