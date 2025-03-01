# d037b0a7 • 002 • example_3 • investigate_coder

---
```python
"""
The transformation takes the colors present in the top row and "drops" them down, filling the corresponding columns below.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replicating non-zero values from the top row
    downwards in their respective columns.
    """
    output_grid = np.copy(input_grid)  # Initialize output_grid as a copy of the input
    rows, cols = input_grid.shape

    # Iterate through the top row (row 0)
    for j in range(cols):
        if input_grid[0, j] != 0:  # Check for non-zero values
            # Replicate the value downwards in the same column
            for i in range(1, rows):
                output_grid[i, j] = input_grid[0, j]

    return output_grid
```
