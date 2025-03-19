# a3df8b1e • 014 • refine_coder

---
```python
"""
The transformation rule identifies the position of a specific blue pixel within the input grid. The rule hinges on the blue pixel being at the top-left corner of a 3x1 rectangle, which can be completed by orange pixels on the right. If this configuration is present, a vertical blue line is drawn in the output grid in the column immediately to the right of the 3x1 rectangle. If there are no blue pixels, or if the specific blue pixel is not present, or is not part of the 3x1 orange extension, the output grid is all zeros (white).
"""

import numpy as np

def find_blue_orange_pattern(grid):
    # Find the coordinates of the specific blue pixel that starts a 3x1 orange extension
    rows = grid.shape[0]
    cols = grid.shape[1]

    for r in range(rows):
        for c in range(cols):
            # Check for blue pixel
            if grid[r, c] == 1:
                # Check for 3x1 orange extension to right, must all exist
                if c + 3 < cols: # bounds check
                    if (grid[r,c+1] == 7) and (grid[r,c+2] == 7) and (grid[r, c+3] == 7):
                        return (r, c) # return the coordinate of the blue
    return None

def transform(input_grid):
    # Initialize the output grid with the same dimensions and all zeros.
    output_grid = np.zeros_like(input_grid)

    # find blue start of orange pattern, could be none
    pattern_start = find_blue_orange_pattern(input_grid)

    # if no pattern, return all white
    if pattern_start == None:
      return output_grid

    # get the column of the blue pixel
    blue_col = pattern_start[1]

    # output column is after the pattern
    output_col = blue_col + 4

    # check output column is in range, otherwise don't add any blue
    if output_col < output_grid.shape[1]:
      # populate all rows of column x with blue
      for row in range(output_grid.shape[0]):
          output_grid[row, output_col] = 1

    return output_grid
```
