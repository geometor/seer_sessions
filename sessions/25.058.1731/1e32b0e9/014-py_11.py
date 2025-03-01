"""
The transformation rule involves expanding blue lines from existing blue and green pixels, stopping at edges or non-zero pixels.
Blue pixels expand both horizontally and vertically. 
Green pixels initiate a vertical expansion of blue *if* there's a blue pixel *anywhere* below it in the same column.
Green pixels initiate horizontal expansion of blue if there's a blue pixel *anywhere* to its right on the same row.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Returns a list of valid (within bounds) neighbors' coordinates (row, col) 
    for a given cell in the grid.  Includes only horizontal and vertical 
    neighbors, not diagonal.
    """
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def expand_blue(grid, row, col):
    """Expands blue horizontally and vertically from the given cell."""
    rows, cols = grid.shape
    
    # Expand Up
    for r in range(row - 1, -1, -1):
        if grid[r, col] == 0:
            grid[r, col] = 1
        else:
            break  # Stop at non-zero

    # Expand Down
    for r in range(row + 1, rows):
        if grid[r, col] == 0:
            grid[r, col] = 1
        else:
            break

    # Expand Left
    for c in range(col - 1, -1, -1):
        if grid[row, c] == 0:
            grid[row, c] = 1
        else:
            break

    # Expand Right
    for c in range(col + 1, cols):
        if grid[row, c] == 0:
            grid[row, c] = 1
        else:
            break

def vertical_expansion(grid, row, col):
    rows, cols = grid.shape
    has_blue_below = False
    for r in range(row + 1, rows):
      if grid[r,col] == 1:
        has_blue_below = True
        break

    if has_blue_below:
      # Expand Up
      for r in range(row - 1, -1, -1):
          if grid[r, col] == 0:
              grid[r, col] = 1
          else:
              break  # Stop at non-zero

      # Expand Down
      for r in range(row + 1, rows):
          if grid[r, col] == 0:
              grid[r, col] = 1
          else:
              break

def horizontal_expansion(grid, row, col):
  rows, cols = grid.shape
  has_blue_right = False
  for c in range(col+1, cols):
    if grid[row,c] == 1:
      has_blue_right = True
      break

  if has_blue_right:
      # Expand Left
      for c in range(col - 1, -1, -1):
          if grid[row, c] == 0:
              grid[row, c] = 1
          else:
              break

      # Expand Right
      for c in range(col + 1, cols):
          if grid[row, c] == 0:
              grid[row, c] = 1
          else:
              break


def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 1. Identify Seeds: Find all blue (1) and green (3) pixels.
    blue_seeds = np.argwhere(output_grid == 1)
    green_seeds = np.argwhere(output_grid == 3)

    # 2.  Blue Expansion
    for row, col in blue_seeds:
        expand_blue(output_grid, row, col)

    # 3. Green Expansion
    for row, col in green_seeds:
        vertical_expansion(output_grid, row, col)
        horizontal_expansion(output_grid, row, col)

    return output_grid