# a5f85a15 • 016 • refine_coder

---
```tool_code
"""
Change maroon (9) pixels to yellow (4) if and only if they are on the top-left to bottom-right diagonal and adjacent to another maroon pixel in that diagonal line.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing maroon (9) pixels to yellow (4)
    if they are on the top-left to bottom-right diagonal and adjacent to
    another maroon pixel in that diagonal line.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    def is_on_top_left_bottom_right_diagonal(row, col, grid):
      """Checks if a pixel is a top-left to bottom-right diagonal"""
      if grid[row,col] != 9:
        return False

      # check above and to the left
      if row > 0 and col > 0 and grid[row-1, col-1] == 9:
        return True

      # check below and to the right
      if row < (rows - 1) and col < (cols - 1) and grid[row+1, col+1] == 9:
        return True
      
      return False

    # Iterate through each pixel
    for row in range(rows):
        for col in range(cols):
            # Check if the pixel is maroon
            if input_grid[row, col] == 9:
                # Check for top-left to bottom-right diagonal adjacency
                if is_on_top_left_bottom_right_diagonal(row, col, input_grid):
                    # Change color to yellow
                    output_grid[row, col] = 4

    return output_grid
```
