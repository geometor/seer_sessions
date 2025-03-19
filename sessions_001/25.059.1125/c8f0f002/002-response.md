# c8f0f002 • 002 • example_3 • investigate_coder

---
```python
"""
Iterates through each cell of the input grid. If a cell's value is '1' or '8', it remains unchanged. Otherwise, the cell's value is changed to '5' in the output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same dimensions as the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each cell of the grid.
    for i in range(rows):
        for j in range(cols):
            # Check the value of the cell.
            if output_grid[i, j] != 1 and output_grid[i, j] != 8:
                # If not 1 or 8, change to 5.
                output_grid[i, j] = 5

    return output_grid
```
