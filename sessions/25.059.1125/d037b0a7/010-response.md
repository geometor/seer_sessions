# d037b0a7 • 010 • example_2 • investigate_coder

---
```python
"""
The transformation rule is to propagate the non-zero colors in each row downwards. 
Specifically, for each non-zero cell in a row, the color of that cell is copied to the cell directly below it in the next row. 
This propagation continues for all subsequent rows. White (0) cells remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by propagating non-zero colors downwards.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each row except the last one
    for r in range(rows - 1):
        # Iterate through each cell in the current row
        for c in range(cols):
            # Check if the current cell is non-zero
            if output_grid[r, c] != 0:
                # Propagate the color downwards
                for r_below in range(r + 1, rows):
                    output_grid[r_below, c] = output_grid[r, c]

    return output_grid
```
