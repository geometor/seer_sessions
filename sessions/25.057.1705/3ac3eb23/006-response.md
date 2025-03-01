# 3ac3eb23 • 006 • refine_coder

---
```python
"""
Iterate through each cell of the input grid.
Identify cells containing a red (2) or azure (8) pixel.
For each identified cell, if the cell directly below exists:
    Copy the color of the current cell to the cell directly below.
The output is the modified grid after processing all cells.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell of the input_grid
    for r in range(rows):
        for c in range(cols):
            # Identify cells with values 2 or 8
            if input_grid[r, c] == 2 or input_grid[r, c] == 8:
                # Copy the value to the cell below, if it exist
                if r + 1 < rows:
                  output_grid[r + 1, c] = input_grid[r, c]
            
    return output_grid
```

