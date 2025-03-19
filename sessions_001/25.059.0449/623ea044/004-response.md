# 623ea044 • 004 • example_1 • investigate_coder

---
```python
"""
Transforms an input grid by creating an inset cross pattern of red pixels (value 2) centered on the location of the original red pixel.
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
    output_grid = np.zeros_like(input_grid)
    origin = find_origin(input_grid)

    if origin is None:
        return output_grid  # Return unchanged if no red pixel is found

    row, col = origin
    height, width = input_grid.shape

    # Draw vertical line
    for i in range(height):
      output_grid[i,col] = 2
    
    # Draw Horizontal line
    for j in range(width):
      output_grid[row,j] = 2
    
    # Draw the inset cross shape
    for i in range(height):
        for j in range(width):
            dist_row = abs(i-row)
            dist_col = abs(j - col)
            if dist_row == dist_col:
              output_grid[i,j] = 2
    
    return output_grid
```
