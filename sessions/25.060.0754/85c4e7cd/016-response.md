# 85c4e7cd • 016 • example_3 • investigate_coder

---
```python
"""
Transforms an input grid to an output grid by swapping colors based on a specific rule.
The transformation identifies the central 2x2 block in the input, uses its color
for the output border, and inverts the colors of the inner layers.
"""

import numpy as np

def transform(input_grid):
    # Create a copy of the input grid to modify.  We will modify the copy and return it as the output
    output_grid = np.copy(input_grid)
    
    # Get the dimensions of the grid
    rows, cols = input_grid.shape
    
    # Get center 2x2 color. We assume the grid size is > 2 for this task
    center_color = input_grid[rows//2, cols//2]

    # Set border color of output
    output_grid[0, :] = center_color
    output_grid[-1, :] = center_color
    output_grid[:, 0] = center_color
    output_grid[:, -1] = center_color

    # Invert other colors based on position
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if input_grid[i, j] == 8:
                output_grid[i, j] = 4
            elif input_grid[i, j] == 1:
                output_grid[i, j] = 2
            elif input_grid[i, j] == 2:
                output_grid[i, j] = 1
            elif input_grid[i, j] == 4:
                output_grid[i,j] = 8

    return output_grid
```
