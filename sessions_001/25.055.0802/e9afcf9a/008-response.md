# e9afcf9a • 008 • example_2 • investigate_coder

---
```python
"""
Creates a checkerboard pattern in the output grid, using the colors of the two input rows. The top-left cell of the output grid should have the same color as the top-left cell of the input grid. Each adjacent cell (horizontally and vertically) should have the alternating color.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid with the same dimensions as the input
    output_grid = np.zeros_like(input_grid)

    # get the colors from the first two rows of the input grid
    color1 = input_grid[0, 0]
    color2 = input_grid[1, 0]

    # iterate through rows and columns to create the checkerboard pattern
    for row in range(input_grid.shape[0]):
        for col in range(input_grid.shape[1]):
            # if row index is even start with color1
            if row % 2 == 0:
              # alternate colors based on column index
              if col % 2 == 0:
                  output_grid[row, col] = color1
              else:
                  output_grid[row, col] = color2
            # if row index is odd, start with color2, using the fact first two colors are distinct
            else:
              if col % 2 == 0:
                  output_grid[row, col] = color2
              else:
                  output_grid[row, col] = color1

    return output_grid
```

