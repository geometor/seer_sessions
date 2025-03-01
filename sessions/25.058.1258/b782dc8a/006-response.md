# b782dc8a • 006 • refine_coder

---
```python
"""
Iterate through each pixel in the input grid.
Identify azure (8) pixels.
For each azure (8) pixel, examine its four immediate neighbors (up, down, left, right).
Check if the adjacent pixel is not an azure (8) pixel.
  - if the non-azure neighbor is white (0) or yellow(4), change the azure pixel to green (3).
  - if the non-azure neighbor is blue (1), change the azure pixel to red (2).
  - If the neighbor is any other color do nothing.
Skip all non-azure pixels - they remain unchanged.
Output - return the modified grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for r in range(rows):
        for c in range(cols):
            # Check if the current pixel is azure
            if input_grid[r, c] == 8:
                # Examine neighbors
                neighbors = []
                if r > 0: neighbors.append((r - 1, c))  # Up
                if r < rows - 1: neighbors.append((r + 1, c))  # Down
                if c > 0: neighbors.append((r, c - 1))  # Left
                if c < cols - 1: neighbors.append((r, c + 1))  # Right

                for nr, nc in neighbors:
                    # if the non-azure neighbor is white (0) or yellow(4), change the azure pixel to green (3).
                    if input_grid[nr, nc] == 0 or input_grid[nr,nc] == 4:
                        output_grid[r, c] = 3
                    # if the non-azure neighbor is blue (1), change the azure pixel to red (2).
                    elif input_grid[nr, nc] == 1:
                        output_grid[r,c] = 2

    return output_grid
```
