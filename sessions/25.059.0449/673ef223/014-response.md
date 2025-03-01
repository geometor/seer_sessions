# 673ef223 • 014 • refine_coder

---
```python
"""
Transforms an input grid by expanding azure regions to the right, constrained by red boundaries and grid edges.
Then, it replaces azure pixels to the right of yellow pixels with yellow on the same row.
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of pixels with the specified color.
    return np.argwhere(grid == color)

def transform(input_grid):
    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 1. & 2. Azure Expansion with Red Boundaries
    for row in range(height):
        azure_pixels = np.where(output_grid[row] == 8)[0]
        if azure_pixels.size > 0:
            start_col = np.min(azure_pixels)
            for col in range(start_col + 1, width):
                if output_grid[row, col] == 2:  # Stop at red
                    break
                output_grid[row, col] = 8

    # 3. Yellow Replacement
    for row in range(height):
        yellow_pixels = np.where(output_grid[row] == 4)[0]
        if yellow_pixels.size > 0:
          first_yellow = np.min(yellow_pixels)
          for col in range(first_yellow + 1, width):
            if output_grid[row, col] == 8:
              output_grid[row, col] = 4
            
    return output_grid
```
