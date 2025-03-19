# d406998b • 020 • example_4 • investigate_coder

---
```python
"""
Iterate through the input grid. Identify gray (5) pixels.
Change gray (5) pixels to green (3) based on these rules:
1. Change the gray pixel in the last column of the top row to green.
2. Change the last gray pixel in the second row to green.
3. Change the gray pixel on the bottom row at column index 2 to green.
4. Change the pixel adjacent to the previously transformed pixel on the bottom row (at the third column) to green.
Preserve all other pixels.
"""

import numpy as np

def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Change the gray pixel in the last column of the top row to green.
    if output_grid[0, cols - 1] == 5:
        output_grid[0, cols - 1] = 3

    # Change the last gray pixel in the second row to green.
     # Iterate backwards to find the last grey
    for j in range(cols -1, -1, -1):
      if output_grid[1,j] == 5:
        output_grid[1, j] = 3
        break

    # Change the gray pixel on the bottom row at column index 2 to green.
    if output_grid[rows - 1, 1] == 5:
        output_grid[rows - 1, 1] = 3

    # Change the pixel adjacent to the previously transformed pixel on the bottom row (at the third column) to green.
    if output_grid[rows - 1, 2] == 5:
        output_grid[rows-1, 2] = 3
        
    return output_grid
```
