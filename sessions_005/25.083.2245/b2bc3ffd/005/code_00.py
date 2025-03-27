"""
Transforms an input grid by shifting all non-orange (7) and non-azure (8) pixels
upwards as much as possible, maintaining their relative order. The remaining
empty spaces (except the bottom row) are then filled with orange (7) pixels.
The bottom row, filled with azure (8), remains unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    bottom_row = rows - 1

    # 1. Identify Mobile Pixels (not orange (7) or azure (8), and not in the bottom row)
    mobile_pixels = []
    for r in range(rows - 1):  # Exclude the bottom row
        for c in range(cols):
            if input_grid[r, c] != 7 and input_grid[r, c] != 8:
                mobile_pixels.append((r, c, input_grid[r, c]))

    # 2. Clear the area where mobile pixels will move (except bottom row)
    for r in range(rows - 1):
      for c in range(cols):
        if output_grid[r,c] != 8:
          output_grid[r,c] = 7

    # 3. Shift Mobile Pixels Upwards
    new_row = 0
    new_col = 0
    for _, _, color in mobile_pixels:
        while new_row < bottom_row and output_grid[new_row, new_col] != 7:
            new_col += 1
            if new_col == cols:
                new_col = 0
                new_row += 1
            if new_row >= bottom_row: # safety
              break

        if new_row < bottom_row:  # Place the pixel
              output_grid[new_row, new_col] = color
              new_col +=1 # move to next spot
              if new_col == cols:
                new_col = 0
                new_row +=1

    return output_grid