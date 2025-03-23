```python
"""
The transformation rule is to shift all non-empty rows in the input grid down by one position, accumulating empty rows (all zeros) at the top. The total number of non-empty rows and the dimensions of the grid remain the same.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid by shifting non-empty rows down."""
    output_grid = np.zeros_like(input_grid)  # Initialize with zeros
    non_empty_rows = []

    # 1. Identify and store Non-Empty Rows:
    for row in input_grid:
        if np.any(row != 0):
            non_empty_rows.append(row)

    # 2. Shift Down (place at the bottom, working upwards):
    num_non_empty = len(non_empty_rows)
    for i in range(num_non_empty):
        output_grid[output_grid.shape[0] - num_non_empty + i, :] = non_empty_rows[i]
    
    return output_grid
```