"""
Extracts the central red and orange colored regions of the input grid, maintains their relative center positions within a new, smaller 3x3 grid, and removes single gray colored pixels. The final output consists of red, orange, and white pixels.
"""

import numpy as np

def get_central_color(grid, color):
    """Finds the color in center row and column, if exists. Returns 0 otherwise"""
    rows, cols = grid.shape
    center_row = rows // 2
    center_col = cols // 2

    if grid[center_row, center_col] == color:
        return color
    else:
        for r in range(rows):
           for c in range(cols):
              if grid[r,c] == color:
                 return color

    return 0

def transform(input_grid):
    """Transforms the input grid according to the rule."""

    # Initialize a 3x3 output grid filled with white (0).
    output_grid = np.zeros((3, 3), dtype=int)

    # Find the central colors in their positions
    red_color = get_central_color(input_grid, 2)
    orange_color = get_central_color(input_grid, 7)
   

    # Place the central red and orange at the corresponding positions, if exist
    if red_color:
      output_grid[0, 1] = red_color
    if orange_color:
      output_grid[2, 1] = orange_color

    return output_grid