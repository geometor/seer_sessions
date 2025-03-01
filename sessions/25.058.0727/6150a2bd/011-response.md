# 6150a2bd • 011 • refine_coder

---
```python
"""
1. **Rotate:** Rotate the input grid 90 degrees counter-clockwise.
2. **Recolor:**
     - If the rotated value is in the last column and not equal to 0, and the row index = 1, change that value to 0.
"""

import numpy as np

def rotate_grid(grid):
    """Rotates a grid 90 degrees counter-clockwise."""
    return np.rot90(grid, k=1)

def transform(input_grid):
    input_grid = np.array(input_grid)
    rotated_grid = rotate_grid(input_grid)  # Rotate the grid
    output_grid = np.copy(rotated_grid) # initialize to rotated grid

    # Recolor based on the rule
    for r in range(output_grid.shape[0]):
        for c in range(output_grid.shape[1]):
            if c == output_grid.shape[1] - 1 and output_grid[r, c] != 0 and r == 1:
                output_grid[r, c] = 0

    return output_grid.tolist() # return as list
```
