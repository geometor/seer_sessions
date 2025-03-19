"""
The central pixel's color propagates outwards in a checkerboard pattern, transforming adjacent pixels. The initial state of the central pixel dictates this checkerboard.
"""

import numpy as np

def get_center(grid):
    """Finds the center coordinates of a grid."""
    rows, cols = grid.shape
    center_row = rows // 2
    center_col = cols // 2
    return center_row, center_col

def transform(input_grid):
    """Transforms the input grid based on a checkerboard expansion from the center."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    center_row, center_col = get_center(input_grid)

    # Preserve the center pixel
    center_color = input_grid[center_row, center_col]
    output_grid[center_row, center_col] = center_color

    # Create a set to store the coordinates of pixels to be processed
    processed = set()
    to_process = [(center_row, center_col)]
    
    while to_process:
      r, c = to_process.pop(0)
      processed.add( (r,c) )

      current_color = output_grid[r, c]
      adjacent_coords = []

      #orthogonal
      if r > 0:
        adjacent_coords.append((r - 1, c))  # Up
      if r < rows - 1:
          adjacent_coords.append((r + 1, c))  # Down
      if c > 0:
          adjacent_coords.append((r, c - 1))  # Left
      if c < cols - 1:
          adjacent_coords.append((r, c + 1))  # Right
      #diagonal
      if r > 0 and c > 0:
          adjacent_coords.append((r-1, c-1))
      if r > 0 and c < cols - 1:
          adjacent_coords.append((r-1, c+1))
      if r < rows - 1 and c > 0:
          adjacent_coords.append((r+1, c-1))
      if r < rows - 1 and c < cols - 1:
        adjacent_coords.append((r+1, c+1))

      for adj_r, adj_c in adjacent_coords:
        if (adj_r, adj_c) not in processed:
          if current_color == 0:
            output_grid[adj_r, adj_c] = 2
          else:
            output_grid[adj_r, adj_c] = 0
          to_process.append( (adj_r, adj_c) )

    return output_grid