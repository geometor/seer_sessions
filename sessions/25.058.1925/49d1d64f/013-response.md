# 49d1d64f • 013 • refine_coder

---
```python
"""
The transformation creates a border around the original grid by duplicating the edge rows and columns.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with expanded dimensions.
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = input_rows + 2, input_cols + 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Copy original grid values to the center of the output grid.
    output_grid[1:output_rows-1, 1:output_cols-1] = input_grid

    # Replicate the first and last rows.
    output_grid[0, 1:output_cols-1] = input_grid[0, :]
    output_grid[-1, 1:output_cols-1] = input_grid[-1, :]

    # Replicate the first and last columns.
    output_grid[1:output_rows-1, 0] = input_grid[:, 0]
    output_grid[1:output_rows-1, -1] = input_grid[:, -1]
    
    # Copy corner pixels
    output_grid[0,0] = input_grid[0,0]
    output_grid[0,-1] = input_grid[0,-1]
    output_grid[-1,0] = input_grid[-1,0]
    output_grid[-1,-1] = input_grid[-1,-1]

    return output_grid
```
