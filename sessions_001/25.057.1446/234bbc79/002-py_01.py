"""
1.  **Identify and Remove:** Locate all gray (5) pixels within the input grid.
2.  **Collapse Columns:** For each column containing a gray pixel, remove that pixel and shift all pixels to the right of the removed pixel one position to the left. This reduces the width of the grid. Do not remove the entire column.
3.  **Preserve Blues:** Preserve the values, in the same positions, of the blue pixel(s) where the value is 1.
4. Preserve Reds: Preserve red pixels that were adjacent to the removed gray pixels.
5. All other pixels are converted to white(0)
"""

import numpy as np

def get_gray_positions(grid):
    # returns a list of (row, col) tuples of positions with gray color
    return np.argwhere(grid == 5)

def shift_left(grid, row, col):
  """Shift elements to the left after removing grey pixel."""
  new_row = np.copy(grid[row,:])
  new_row = np.delete(new_row, col)
  new_row = np.append(new_row, 0)  #append white at the end

  return new_row

def transform(input_grid):
    # initialize output_grid

    # get positions of the gray pixels in the grid
    gray_positions = get_gray_positions(input_grid)

    # create copy of the input grid
    output_grid = np.copy(input_grid)

    # remove gray pixels by and shifting to the left
    cols_removed = 0
    for r, c in gray_positions:
      output_grid[r] = shift_left(output_grid, r, c-cols_removed)
      cols_removed +=1

    # remove the extra end columns created by the shift, equal to count of removed
    output_grid = output_grid[:, :-cols_removed]

    # Preserve blues, converting others to white:
    for r in range(output_grid.shape[0]):
      for c in range(output_grid.shape[1]):
        if output_grid[r,c] != 1 and output_grid[r,c] != 2:
          output_grid[r,c] = 0


    return output_grid