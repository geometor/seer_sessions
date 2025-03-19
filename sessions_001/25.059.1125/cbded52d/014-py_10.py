"""
The transformation rule involves moving all green pixels (value 3) to the bottom of their respective columns, while leaving all other pixels (non-green) unaltered.
"""

import numpy as np

def move_greens_to_bottom(grid):
    """Moves all green pixels to the bottom of their respective columns, preserving other pixels."""
    rows, cols = grid.shape
    new_grid = np.copy(grid)  # Work on a copy

    # Iterate by column
    for c in range(cols):
      # Collect non-green pixels and their original row indices in this column
      non_green_pixels = []
      for r in range(rows):
          if new_grid[r, c] != 3:
              non_green_pixels.append((r, new_grid[r, c]))

      # Count green pixels in this column
      num_greens = rows - len(non_green_pixels)
      
      #rewrite the column
      row_index = 0
      #first the non-green pixels, maintaining original order
      for (orig_row, pixel_val) in non_green_pixels:
        new_grid[row_index,c] = pixel_val
        row_index += 1
      #fill the rest with green pixels
      for i in range(num_greens):
        new_grid[row_index,c] = 3
        row_index += 1

    return new_grid

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Move green pixels to the bottom, preserving others
    output_grid = move_greens_to_bottom(output_grid)

    return output_grid