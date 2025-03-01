# 1f0c79e5 • 004 • example_1 • investigate_coder

---
```python
"""
1. **Identify the non-zero pixels:** Locate all pixels in the input grid that have a value other than 0.
2.  **Change Red to Yellow:**  If there's a red (2) pixel, change its color to yellow (4).
3. **Center:** Imagine the smallest bounding square that can contain a 3x3 object within the 9x9 grid.
4.  **Create a 3x3 Yellow Square:** Create a filled 3x3 square of yellow (4) pixels.
5.  **Fill the Background:** Fill the rest of the grid, all remaining pixels, with 0 (white).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing non-zero pixels with a 3x3 yellow square.
    """
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Change Red to Yellow
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] == 2:
                input_grid[i,j] = 4

   # Create a 3x3 Yellow Square, Centered Horizontally, near the top

    for i in range(3):
        for j in range(3):
                output_grid[i,j+cols-3] = 4

    return output_grid
```
