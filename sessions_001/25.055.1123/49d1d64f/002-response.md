# 49d1d64f • 002 • example_1 • investigate_coder

---
```python
"""
Expands a 2x2 input grid into a 4x4 output grid. Each cell in the input grid is replicated as a 2x2 block in the output grid, and a white (0) border is added.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a 4x4 array filled with white (0).
    output_grid = np.zeros((4, 4), dtype=int)

    # Iterate through each cell of the input grid.
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            # Replicate the input cell's color to a 2x2 block in the output grid.
            output_grid[2*i:2*i+2, 2*j:2*j+2] = input_grid[i, j]
            
            # set correct start positions:
            output_grid[2*i+1, 2*j+1] = input_grid[i,j]
            output_grid[2*i+1, 2*j] = input_grid[i,j]
             
    return output_grid
```
