# 8f2ea7aa • 010 • example_2 • investigate_coder

---
```python
"""
The transformation rule involves mirroring the orange pixels (value 7) in the input grid across horizontal, vertical, and diagonal axes.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by mirroring the orange pixels across horizontal, vertical, and diagonal axes.
    """
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Find the coordinates of orange pixels
    orange_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 7:
                orange_pixels.append((r, c))

    # Mirror across horizontal and vertical axes
    for r, c in orange_pixels:
        # Horizontal mirror
        output_grid[r, cols - 1 - c] = 7
        # Vertical mirror
        output_grid[rows - 1 - r, c] = 7
        # Both
        output_grid[rows - 1- r, cols - 1 - c] = 7
        
    # Mirror the original orange across diagonals
    for r, c in orange_pixels:
      output_grid[c,r] = 7
      output_grid[(cols-1)-c, (rows-1)-r] = 7
        
    #ensure original orange pixels are in the output
    for r, c in orange_pixels:
      output_grid[r,c] = 7

    return output_grid
```
