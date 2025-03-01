# 6f8cd79b • 008 • example_2 • investigate_coder

---
```python
"""
The transformation rule is to change the boundary pixels of the input grid to color 8 (azure), while leaving the inner pixels unchanged.  For a 3x3 grid, this effectively creates an azure frame around the original content.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing the boundary pixels to color 8,
    leaving the inner pixels unchanged.
    """
    output_grid = np.copy(input_grid)  # Create a copy to avoid modifying the original
    rows, cols = output_grid.shape

    # Iterate through all pixels
    for i in range(rows):
        for j in range(cols):
            # Check if the pixel is on the boundary
            if i == 0 or i == rows - 1 or j == 0 or j == cols - 1:
                output_grid[i, j] = 8  # Change boundary pixel color to 8

    return output_grid
```
