# 6150a2bd • 002 • example_1 • investigate_coder

---
```python
"""
The transformation preserves the 3x3 grid structure and the central element. 
All other elements are mirrored across both the horizontal and vertical axes (or rotated 180 degrees).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Get the dimensions of the grid
    rows, cols = output_grid.shape

    # Iterate through the grid, skipping the center element
    for i in range(rows):
        for j in range(cols):
            # Mirror the elements (or rotate by 180 degrees)
            output_grid[i, j] = input_grid[rows - 1 - i, cols - 1 - j]

    return output_grid
```
