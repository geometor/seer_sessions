"""
Transforms a grid with sparse red pixels into a grid with nested red squares,
centered on the original red pixel's location.
"""

import numpy as np

def find_red_pixels(grid):
    """Finds the coordinates of red pixels in the grid."""
    return np.argwhere(grid == 2)

def create_nested_squares(grid, center):
    """Creates nested squares centered on the given center."""
    rows, cols = grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)
    
    # Find max possible size for square
    max_size = min(rows, cols)

    # Iterate to draw nested squares. Stop when center is a pixel
    for size in range(max_size, 0, -2):
      top = center[0] - size // 2
      left = center[1] - size // 2
      bottom = top + size
      right = left + size

      #check boundary conditions
      if top < 0 or left < 0:
        continue
      if bottom > rows or right > cols:
        continue

      # Draw square outline (handling edge cases)
      for i in range(max(0, left), min(right, cols)):
          if top >= 0 and top < rows:
            output_grid[top,i] = 2
          if bottom-1 >=0 and bottom -1 < rows:
            output_grid[bottom - 1, i] = 2
      for i in range(max(0, top), min(bottom, rows)):
          if left >= 0 and left < cols:
            output_grid[i, left] = 2
          if right-1 >=0 and right-1 < cols:
            output_grid[i, right - 1] = 2
    return output_grid

def transform(input_grid):
    """
    Transforms the input grid by creating a nested squares pattern of red pixels,
    centered on the original red pixel's location.
    """
    # Find red pixels
    red_pixels = find_red_pixels(input_grid)

    # If no red pixels, return a blank grid (or a copy of input)
    if len(red_pixels) == 0:
        return np.zeros_like(input_grid)

    # Create nested squares based on *first* red pixel
    output_grid = create_nested_squares(input_grid, red_pixels[0])

    return output_grid