# 3ac3eb23 • 002 • example_1 • investigate_coder

---
```python
"""
Iterate through each cell of the input grid.
Identify cells with the values 2 (red) or 8 (azure).
For each identified cell:
    Copy the value of the colored pixel to the cell immediately below it in the next row.
Preserve all other cells (value 0 (white)) as they are.
The final output is the modified version of the grid.
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
