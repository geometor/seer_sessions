# 94f9d214 • 022 • refine_coder

---
```python
"""
1.  **Locate Non-White Pixel:** Find the single non-white pixel in the input grid.
2.  **Output Grid:** Create a 1x1 output grid.
3.  **Copy Color:** Copy the color of the located non-white pixel to the output grid's single cell.
"""

import numpy as np

def find_non_white_pixel(grid):
    # Iterate through the grid to find the first non-white pixel
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] != 0:
                return i, j, grid[i, j]
    return None, None, None  # Return None if no non-white pixel is found

def transform(input_grid):
    # Convert input to numpy array
    grid = np.array(input_grid)

    # Find the non-white pixel and its color
    row, col, color = find_non_white_pixel(grid)

    # Create a 1x1 output grid
    output_grid = np.zeros((1, 1), dtype=int)

    # If a non-white pixel was found, set the output grid's cell to its color
    if row is not None:
        output_grid[0, 0] = color

    return output_grid.tolist()
```
