"""
Transforms the input grid based on the presence or absence of a red horizontal line.

1.  **Check for Red Object:** Determine if a horizontal red (2) line exists in the input grid.

2.  **Conditional Actions:**

    *   **If a red object is present:**
        *   Create a green (3) rectangle directly above the red object. The rectangle's width is equal to the red line's length plus one. Its height is 2. It is left-aligned with the red object.
        *   Create a blue (1) vertical line directly below the red object. The line's height is 3, and its width is 1. It is left-aligned with the red object.

    *   **If a red object is NOT present:**
        *   Create a green (3) rectangle spanning the top two rows of the grid.  The rectangle's width is equal to the input grid's width minus 2. The height is 2.
        *   Create a blue (1) vertical line of height 1 at the bottom-left corner (row = height-1, col = 0) of the grid.

3.  **Preservation:** Any pixels not modified by the above rules should remain unchanged (white (0)).
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
    output_grid[:] = 0 # Initialize to all white
    
    # Find red object
    red_row, red_col_start, red_length = find_red_object(input_grid)
    
    if red_row is not None:
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

        # Create the blue vertical line.
        blue_height = 3
        blue_row_start = red_row + 1

        if blue_row_start < output_grid.shape[0]:
            for i in range(blue_height):
                if blue_row_start + i < output_grid.shape[0]:
                    output_grid[blue_row_start + i, red_col_start] = 1
    else:
        # No red object present
        # Create green rectangle at the top
        green_height = 2
        green_width = input_grid.shape[1] - 2  # Use input grid width - 2
        for r in range(green_height):
            for c in range(green_width):
                output_grid[r, c] = 3

        # Create blue vertical line at the bottom-left
        blue_height = 1
        output_grid[output_grid.shape[0] - 1, 0] = 1 #single pixel
    return output_grid