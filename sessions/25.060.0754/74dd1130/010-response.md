# 74dd1130 • 010 • example_2 • investigate_coder

---
```python
"""
Iterate through each pixel of the input grid. For each pixel, check if its left neighbor exists. If the current pixel's color is red (2) and the left neighbor's color is magenta (6), or vice-versa, swap the colors of the current pixel and its left neighbor. Otherwise, the pixel's color remains the same. Output the transformed grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each pixel of the input grid
    for r in range(rows):
        for c in range(cols):
            # Consider the left neighbor
            if c > 0:  # Check if left neighbor exists
                # If the current pixel is red and the left neighbor is magenta, swap
                if output_grid[r, c] == 2 and output_grid[r, c - 1] == 6:
                    output_grid[r, c] = 6
                    output_grid[r, c - 1] = 2
                # If the current pixel is magenta and the left neighbor is red, swap
                elif output_grid[r, c] == 6 and output_grid[r, c - 1] == 2:
                    output_grid[r, c] = 2
                    output_grid[r, c - 1] = 6
            # Otherwise, pixel remains unchanged.
    return output_grid
```
