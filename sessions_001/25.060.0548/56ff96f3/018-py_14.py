"""
The transformation identifies isolated yellow pixels in the input grid, determines a bounding box 
encompassing these pixels, and then fills this bounding box with yellow pixels in the output grid.
"""

import numpy as np

def get_yellow_pixels(grid):
    """Finds the coordinates of all yellow pixels in the grid."""
    yellow_pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 4:
                yellow_pixels.append((r, c))
    return yellow_pixels

def bounding_box(pixels):
    """Calculates the bounding box of a list of pixel coordinates."""
    if not pixels:
        return None
    min_row, min_col = float('inf'), float('inf')
    max_row, max_col = float('-inf'), float('-inf')
    for r, c in pixels:
        min_row = min(min_row, r)
        max_row = max(max_row, r)
        min_col = min(min_col, c)
        max_col = max(max_col, c)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    """
    Transforms the input grid by identifying yellow pixels, forming a bounding box, and filling it with yellow.
    """
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find yellow pixels
    yellow_pixels = get_yellow_pixels(input_grid)

    # Determine bounding box
    if yellow_pixels:
      top_left, bottom_right = bounding_box(yellow_pixels)

      # Fill bounding box in output grid
      for r in range(top_left[0], bottom_right[0] + 1):
          for c in range(top_left[1], bottom_right[1] + 1):
              output_grid[r, c] = 4

    return output_grid