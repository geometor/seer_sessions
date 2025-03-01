"""
Transforms the input grid by creating green and blue objects relative to a red object.

1. **Identify the Red Object:** Locate the horizontal line of red (2) pixels. Note its length and starting position.
2. **Create the Green Object:** Above the red object, create a green (3) rectangular block.
  - The green block's width is one pixel wider than the red object.
  - The green block's height is two rows.
  - The green block's left edge aligns with red objects left edge.
3. **Create the Blue Object:** Below the red object, create a blue (1) L-shaped block.
 - The top of the L aligns with the bottom of the red object.
 - It consists of three stacked blue pixels.
4. **Retain Unchanged Pixels**: All white pixels (0) that are not part of the generated objects remain as 0.
"""

import numpy as np

def find_red_object(grid):
    # Find the red object (horizontal line of 2s)
    red_rows, red_cols = np.where(grid == 2)
    if len(red_rows) == 0:
      return None, 0, 0
    min_col = np.min(red_cols)
    max_col = np.max(red_cols)
    return red_rows[0], min_col, max_col - min_col + 1

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # Find red object
    red_row, red_col_start, red_length = find_red_object(input_grid)
    
    if red_row is None:
        return output_grid

    # Create green object
    green_width = red_length + 1
    green_height = 2
    green_row_start = red_row - green_height
    green_col_start = red_col_start
    
    if green_row_start >= 0:
      for r in range(green_height):
          for c in range(green_width):
              if green_col_start + c < output_grid.shape[1]:
                  output_grid[green_row_start + r, green_col_start + c] = 3

    # Create the blue L-Shaped object.
    blue_height = 3
    blue_row_start = red_row + 1

    if blue_row_start < output_grid.shape[0]:
        for i in range(blue_height):
            if blue_row_start + i < output_grid.shape[0]:
                output_grid[blue_row_start + i, red_col_start] = 1

    return output_grid