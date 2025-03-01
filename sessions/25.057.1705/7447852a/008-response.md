# 7447852a • 008 • example_2 • investigate_coder

---
```python
"""
1.  **Identify Red Pixels:** Locate all pixels with the color red (value 2) in the input grid.

2.  **Horizontal Adjacency Check (Left/Right):** For each red pixel, check if it has a horizontally adjacent white pixel (value 0).

    *   If there is a white pixel adjacent to the red pixel to its right, change the white box to its right to yellow.
    *   If there is a white pixel adjacent to the red pixel to its left, change the white box to its left to yellow.

3.  **Vertical Adjacency Check (Above/Below** For each red pixel, check if it has a vertically adjacent white pixel (value 0)

    *   If there is a white pixel adjacent to the red pixel above it, change the white box above it to yellow
    *   If there is a white pixel adjacent to the red pixel below it, change the white box below it to yellow.

4. **Diagonal Adjacency Check:** If there are white pixels diagonal to any red pixel do NOT change it to yellow.
5.  **Preserve Other Pixels:** All other pixels that are not horizontally or vertically adjacent to a red pixel remain unchanged.
6.  **Output:** The resulting grid is the output, containing red, white, and yellow pixels based on the adjacency rule.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # change output pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 2:  # Find red pixels
                # Check horizontal adjacency (left/right)
                if c > 0 and input_grid[r, c-1] == 0:
                    output_grid[r, c-1] = 4
                if c < cols - 1 and input_grid[r, c+1] == 0:
                    output_grid[r, c+1] = 4
                # Check vertical adjacency (above/below)
                if r > 0 and input_grid[r-1, c] == 0:
                    output_grid[r-1, c] = 4
                if r < rows - 1 and input_grid[r+1, c] == 0:
                    output_grid[r+1, c] = 4

    return output_grid
```
