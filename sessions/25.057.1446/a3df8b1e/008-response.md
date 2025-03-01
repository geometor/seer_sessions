# a3df8b1e • 008 • example_2 • investigate_coder

---
```python
"""
The transformation rule involves identifying a single blue pixel in the input grid and generating a specific, diagonally repeating pattern of blue pixels in the output grid, starting from the location of the initial blue pixel.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same dimensions as the input grid, filled with zeros (white).
    output_grid = np.zeros_like(input_grid)

    # Find the location of the blue pixel (value 1) in the input grid.
    blue_pixel_location = np.where(input_grid == 1)
    
    # start populating output grid from bottom left
    row = input_grid.shape[0] - 1
    col = 0

    # The pattern '1' placement can be described by alternating placement along x % 2 == 0, if not, then x+1
    while row >= 0:
      output_grid[row, col] = 1
      if row % 2 == 0:
          row -= 1
          col = 1
      else:
        if col == 1:
            row -= 2
            col = 0
        else:
            row -=1
            col = 2
            
    return output_grid
```
