# 28e73c20 • 014 • example_2 • investigate_coder

---
```python
"""
The transformation rule is as follows:
1. Create a green (3) border around the 8x8 grid.
2. Fill the specific cells inside the border with green to make filled square and cross shape.
3. Keep all other original white(0) pixels unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape

    # Create the green border.
    for i in range(height):
        for j in range(width):
            if i == 0 or i == height - 1 or j == 0 or j == width - 1:
                output_grid[i, j] = 3

    # Inner square and cross.
    output_grid[2, 2:6] = 3
    output_grid[3, 2] = 3
    output_grid[3, 5] = 3
    output_grid[4, 2] = 3
    output_grid[4, 3] = 3
    output_grid[4, 5] = 3
    output_grid[5, 2:6] = 3
    
    return output_grid
```
