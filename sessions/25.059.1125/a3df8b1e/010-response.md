# a3df8b1e • 010 • example_2 • investigate_coder

---
```python
"""
The transformation rule involves identifying a single blue pixel in the input grid and generating a repeating pattern of blue pixels in the output grid. The pattern alternates between the first and second columns for the first three rows, then switches to column 2, and repeats this four-step sequence.
"""

import numpy as np

def find_blue_pixel(grid):
    # Find the coordinates of the blue pixel (value 1).
    for r in range(grid.shape[0]):
      for c in range(grid.shape[1]):
        if grid[r][c] == 1:
          return (r,c)
    return None

def transform(input_grid):
    # Initialize the output grid with the same dimensions and all zeros.
    output_grid = np.zeros_like(input_grid)

    # find blue, could be none
    blue_pixel = find_blue_pixel(input_grid)

    # if no blue, return all white
    if blue_pixel==None:
      return output_grid

    # Create the repeating pattern.
    for row in range(output_grid.shape[0]):
        if row % 4 == 0:
          output_grid[row, 1] = 1
        elif row % 4 == 1:
          output_grid[row, 0] = 1
        elif row % 4 == 2:
            output_grid[row,1] = 1
        elif row % 4 == 3:
            output_grid[row, 2] = 1


    return output_grid
```
