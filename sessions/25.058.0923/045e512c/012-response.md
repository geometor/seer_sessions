# 045e512c • 012 • refine_coder

---
```python
"""
Transforms an input grid by expanding and replicating red and yellow pixels around a central blue pixel. Red pixels fill horizontally and are mirrored vertically. Yellow pixels fill vertically and extend diagonally if initially diagonal to the blue pixel. The blue pixel is moved to the center row.
"""

import numpy as np

def find_center(grid):
    # Find the blue pixel, assumed to be the center
    blue_pixels = np.argwhere(grid == 1)
    if blue_pixels.size == 0:
      return None
    return blue_pixels[0]

def fill_red(grid, center):
  output_grid = np.copy(grid)
  rows, cols = grid.shape
  center_row, center_col = center

  red_pixels = np.argwhere(grid == 2)

  for r_pix in red_pixels:
    # Extend red to left edge
    for c in range(0, r_pix[1] + 1):
        output_grid[r_pix[0], c] = 2
    #Mirror Row
    mirrored_row = center_row + (center_row - r_pix[0])
    if 0 <= mirrored_row < rows:
      for c in range(cols):
        output_grid[mirrored_row,c] = 2

  return output_grid

def fill_yellow(grid, center):
  output_grid = np.copy(grid)
  rows, cols = output_grid.shape
  center_row, center_col = center

  yellow_pixels = np.argwhere(grid == 4)
  for y_pix in yellow_pixels:
      # Vertical fill
      for r in range(rows):
        output_grid[r,y_pix[1]] = 4

      # Diagonal fill
      row_offset = y_pix[0] - center_row
      col_offset = y_pix[1] - center_col

      if row_offset != 0 and col_offset != 0:  # Check for diagonal adjacency
            dr = row_offset // abs(row_offset) # direction
            dc = col_offset // abs(col_offset)
            current_row = y_pix[0]
            current_col = y_pix[1]

            while 0 <= current_row < rows and 0 <= current_col < cols:
                output_grid[current_row, current_col] = 4
                current_row += dr
                current_col += dc

            # mirror
            mirrored_row = center_row - row_offset
            mirrored_col = center_col - col_offset
            if 0 <= mirrored_row < rows and 0 <= mirrored_col < cols:
                current_row = mirrored_row
                current_col = mirrored_col
                while 0 <= current_row < rows and 0 <= mirrored_col < cols:
                  output_grid[current_row, current_col] = 4
                  current_row -= dr
                  current_col -= dc

  return output_grid

def move_center(grid, center):
    output_grid = np.copy(grid)
    rows, _ = grid.shape
    center_row, center_col = center

    new_center_row = rows // 2
    output_grid[center_row, center_col] = 0  # Clear original center
    output_grid[new_center_row, center_col] = 1 # Place in new center

    return output_grid

def fill_between_red(grid):
  output_grid = np.copy(grid)
  rows,cols = output_grid.shape
  red_rows = np.unique(np.argwhere(output_grid == 2)[:,0])

  for r in range(rows):
    if r not in red_rows:
      for c in range(cols):
        output_grid[r,c] = 0

  for i in range(len(red_rows) - 1):
    for r in range(red_rows[i] + 1, red_rows[i+1]):
      for c in range(cols):
        if output_grid[r,c] != 4:
            output_grid[r,c] = 2
  return output_grid

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find the center (blue pixel)
    center = find_center(input_grid)
    if center is None:
        return output_grid

    # Fill Yellow Component
    output_grid = fill_yellow(output_grid, center)

    # Fill Red Component
    output_grid = fill_red(output_grid, center)

    # fill between the red
    output_grid = fill_between_red(output_grid)

    # Move Blue to Vertical Center
    output_grid = move_center(output_grid, center)

    return output_grid
```
