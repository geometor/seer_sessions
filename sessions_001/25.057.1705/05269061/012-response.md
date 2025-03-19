# 05269061 • 012 • refine_coder

---
```python
"""
The transformation rule discards the contents of the input grid entirely. The output grid always has the same dimensions as the input grid.  The output grid is filled with a repeating checkerboard pattern using the colors 2 (red), 4 (yellow), and 1 (blue). The pattern starts with 2 (red) in the top-left cell and alternates. The input grid's colors and pattern have no influence on the output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid with the same dimensions as the input grid
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = np.zeros((rows, cols), dtype=int)

    # fill the output grid with the checkerboard pattern
    for row in range(rows):
        for col in range(cols):
            # determine the color based on row and column
            if (row + col) % 3 == 0:
                output_grid[row, col] = 2  # red
            elif (row + col) % 3 == 1:
                output_grid[row, col] = 4  # yellow
            else:
                output_grid[row, col] = 1  # blue

    return output_grid
```

