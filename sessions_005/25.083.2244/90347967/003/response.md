```python
"""
The transformation reverses the order of non-zero elements within each row of the input grid and then right-aligns them in the output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Row-wise Processing
    for i in range(rows):
        row_values = input_grid[i]
        # Identify Non-Zero Elements
        non_zero_values = row_values[row_values != 0]
        # Reverse Sub-row
        reversed_non_zero = non_zero_values[::-1]
        # Right-Shift
        num_zeros = len(row_values) - len(reversed_non_zero)
        new_row = np.concatenate((np.zeros(num_zeros), reversed_non_zero))
        # Assign
        output_grid[i] = new_row

    return output_grid.tolist()
```
