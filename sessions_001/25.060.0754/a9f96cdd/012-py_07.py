"""
1.  Identify the non-white pixel within the input grid.
2.  Determine the new color of the pixel based on a cyclic sequence: Red (2) -> Green (3) -> Yellow (4) -> Red (2)...
3.  Calculate the new position by moving one step up and one step to the left.
4.  Apply wraparound:
    *   If the new row index is -1, set it to height of grid - 1.
    *   If the new column index is -1, set it to width of grid- 1.
5.  All other pixels in the grid should be set to White (0).
6. Return new grid.
"""

import numpy as np

def find_colored_pixel(grid):
    # Find the coordinates of the non-zero pixel.
    rows, cols = np.where(grid != 0)
    if len(rows) > 0:  # Ensure a non-zero pixel was found
      return rows[0], cols[0], grid[rows[0], cols[0]] # return row, col, and color
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    height = input_grid.shape[0]
    width = input_grid.shape[1]


    # Find the colored pixel in the input grid.
    colored_pixel_coords = find_colored_pixel(input_grid)

    if colored_pixel_coords:
      # change output pixels
      row, col, color = colored_pixel_coords
      new_row = (row - 1) % height # wrap rows
      new_col = (col - 1) % width # wrap cols
      new_color = {
          2: 3,  # Red to Green
          3: 4,  # Green to Yellow
          4: 2,  # Yellow to Red
      }.get(color)
      output_grid[new_row, new_col] = new_color


    return output_grid