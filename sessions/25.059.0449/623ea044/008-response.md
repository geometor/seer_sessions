# 623ea044 • 008 • refine_coder

---
```python
"""
Transforms an input grid by identifying the location of the red pixel (value 2) and drawing two lines of red pixels. One horizontal line extends to the right, and the other vertical line extends downwards, both from the position of the original red pixel.  The lines stop when they encounter a non-white pixel (a pixel with a value other than 0) or the edge of the grid.
"""

import numpy as np

def find_origin(grid):
    # Find the coordinates of the single red pixel (value 2)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 2:
                return (i, j)
    return None

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    output_grid = np.array(input_grid, copy=True)  # Start with a copy, modify copy
    origin = find_origin(input_grid)

    if origin is None:
        return output_grid  # Return unchanged if no red pixel is found

    row, col = origin
    height, width = input_grid.shape

    # Draw vertical line downwards
    for i in range(row, height):
        if output_grid[i, col] != 0 and i != row:  # Check for non-white pixel (and not the origin itself)
            break  # Stop if a non-white pixel is encountered
        output_grid[i, col] = 2

    # Draw Horizontal line to the right
    for j in range(col, width):
        if output_grid[row, j] != 0 and j != col: # Check for non-white pixel (and not the origin itself)
            break  # Stop if a non-white pixel is encountered
        output_grid[row, j] = 2

    return output_grid
```

