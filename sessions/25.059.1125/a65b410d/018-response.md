# a65b410d • 018 • refine_coder

---
```python
"""
Transforms the input grid based on the presence or absence of a red horizontal line.

1.  **Check for Red Object:** Check if a horizontal red (2) line exists.
2.  **Conditional Actions:**
    *   **If a red object is present:**
        *   Create a green (3) rectangle above the red object (width = red length + 1, height = 2, left-aligned).
        *   Create a blue (1) vertical line of length 3 below the red object (left-aligned).
    *   **If a red object is NOT present:**
        *   Create a green (3) rectangle at the top of the grid (row 0).  The width should be determined by observing input and output. The height is 2.
        *   Create a blue (1) vertical line of height 3 at the bottom-left corner of the grid.
3. **Retain Unchanged Pixels**: All white (0) pixels not part of created objects should remain white.
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
        green_width = input_grid.shape[1] # Use input grid width
        for r in range(green_height):
            for c in range(green_width):
                output_grid[r, c] = 3

        # Create blue vertical line at the bottom-left
        blue_height = 3
        for i in range(blue_height):
            if output_grid.shape[0] - 1 - i >= 0:
               output_grid[output_grid.shape[0] - 1 - i, 0] = 1
    return output_grid
```
