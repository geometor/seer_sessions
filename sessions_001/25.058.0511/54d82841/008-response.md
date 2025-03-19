# 54d82841 • 008 • example_2 • investigate_coder

---
```python
"""
A single white pixel at the bottom is recolored to yellow.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Get the dimensions of the grid
    rows, cols = output_grid.shape

    # Locate the specific white pixel to change: last row, middle column
    #  (adjusting for zero-based indexing).
    target_row = rows - 1
    target_col = cols // 2

    # Change the color of the target pixel to yellow (4)
    output_grid[target_row, target_col] = 4

    return output_grid
```
