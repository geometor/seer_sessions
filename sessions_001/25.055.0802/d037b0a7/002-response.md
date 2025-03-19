# d037b0a7 • 002 • example_1 • investigate_coder

---
```python
"""
Iterate through each column of the input grid.  Within each column, find the
highest row index that has non-zero values.  Propagate these values downwards
replacing all zero values to fill the column.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each column
    for j in range(cols):
        # Find the highest row index with a non-zero value
        for i in range(rows):
            if output_grid[i, j] != 0:
                # Propagate the non-zero value downwards
                for k in range(i + 1, rows):
                    output_grid[k, j] = output_grid[i, j]
                
    return output_grid
```
