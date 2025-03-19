# 794b24be • 008 • example_2 • investigate_coder

---
```python
"""
1.  **Identify Blue Pixels:** Examine each pixel in the input grid.
2.  **First Row Rule, apply to blue pixels**: If a blue pixel is in the first row, change its color to red.
3. **Adjacent to changed**: Then, if a pixel is now red, all blue pixels that were originally next to it are also changed to red
4.  **All other pixels:** Maintain their original color.
"""

import numpy as np

def get_neighbors(grid, row, col):
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            r, c = row + i, col + j
            if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]:
                neighbors.append((r, c))
    return neighbors

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # keep track of changes to re-check neighbors
    changed_pixels = []

    # First pass for first-row blue pixels
    for col in range(cols):
        if input_grid[0, col] == 1:
            output_grid[0, col] = 2
            changed_pixels.append((0,col))

    #check adjacent pixels to changed ones
    for r, c in changed_pixels:
        neighbors = get_neighbors(input_grid, r, c)
        for nr, nc in neighbors:
            if input_grid[nr, nc] == 1:
                output_grid[nr, nc] = 2


    return output_grid
```
