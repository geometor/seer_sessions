# b782dc8a • 008 • refine_coder

---
```python
"""
Iterate through each pixel in the input grid.

1.  **Identify Azure Pixels:** Check if the current pixel's color is azure (8).
2.  **Examine Neighbors:** If the pixel is azure, examine its four immediate neighbors (up, down, left, and right).
3.  **Conditional Color Change:**
     *  If a neighbor's color is blue (1), change the azure pixel's color to red (2).
     *  If a neighbor's color is white (0) or yellow(4) change the azure pixel's color to green(3)
4. **Skip Non-Azure Pixels**: If a pixel is not azure it is unchanged.
5. **Output**: Return the modified grid
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
