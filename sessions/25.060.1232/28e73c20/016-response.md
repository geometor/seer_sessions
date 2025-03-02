# 28e73c20 • 016 • refine_coder

---
```python
"""
1. Copy the input grid to the output grid.
2. Create a green (value 3) border around the grid by setting the values of the outermost rows and columns to 3.
3. Fill the area inside the border with green color.
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

    # Fill the inner area with green.
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            output_grid[i, j] = 3
    
    return output_grid
```

