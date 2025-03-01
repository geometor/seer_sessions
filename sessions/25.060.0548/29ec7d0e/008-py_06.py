"""
1.  Identify Rectangles: Locate the rectangle defined by contiguous pixels of value `0`.
2.  Replace with Background: Change the value of all pixels within the identified rectangle to `1` (blue).
3.  Output: The final grid consists of the original gray pixels, with the identified rectangle replaced with blue.
"""

import numpy as np

def find_rectangle(grid, color=0):
    """Finds the bounding box of a contiguous region of the specified color."""
    rows, cols = grid.shape
    min_row, min_col = rows, cols
    max_row, max_col = -1, -1

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                min_row = min(min_row, r)
                min_col = min(min_col, c)
                max_row = max(max_row, r)
                max_col = max(max_col, c)

    if max_row == -1: # No rectangle found
        return None
    
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    """Transforms the input grid by replacing a 0-value rectangle with blue (1)."""

    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    background_color = 1

    # 1. Identify Rectangle.
    rectangle_bounds = find_rectangle(output_grid, color=0)

    # 2. Replace with Background.
    if rectangle_bounds:
      (min_row, min_col), (max_row, max_col) = rectangle_bounds
      for r in range(min_row, max_row + 1):
          for c in range(min_col, max_col + 1):
              output_grid[r, c] = background_color

    return output_grid