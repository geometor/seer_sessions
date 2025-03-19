# 49d1d64f • 018 • refine_coder

---
```python
"""
Expands the input grid by adding one row and one column of black pixels (color 0) around it. The input grid is placed in the top-left corner of the output grid.
"""

import numpy as np

def transform(input_grid):
    # Determine the dimensions of the input grid.
    input_rows, input_cols = input_grid.shape

    # Calculate the dimensions of the output grid.
    output_rows = input_rows + 1
    output_cols = input_cols + 1

    # Create the output grid, filled with black pixels (color 0).
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Copy the input grid to the top-left corner of the output grid.
    for i in range(input_rows):
        for j in range(input_cols):
            output_grid[i, j] = input_grid[i, j]

    return output_grid
```

