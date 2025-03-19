# f25ffba3 • 010 • example_2 • investigate_coder

---
```python
"""
The transformation involves mirroring the bottom half of the input grid (excluding the rightmost red column) 
to the top half of the output grid, while keeping the rightmost red column unchanged.
"""

import numpy as np

def find_red_column(grid):
    # Find the rightmost column with all red (2) pixels
    height, width = grid.shape
    for j in reversed(range(width)):
        if np.all(grid[:, j] == 2):
            return j
    return -1  # Should not happen in this task, but good practice to handle

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    
    # Find the red column index
    red_column_index = find_red_column(input_grid)

    # Mirror the bottom half (excluding the red column) to the top half
    half_height = height // 2
    for i in range(half_height):
        for j in range(width):
            if j != red_column_index:
                output_grid[i, j] = input_grid[height - 1 - i, j]

    return output_grid
```
