# 99fa7670 • 012 • refine_coder

---
```python
"""
1.  **Identify the Source Pixel:** If there is only one non-white pixel within the input grid, consider its color and location as the source. If there are multiple, no action.
2.  **Conditional Replication:** If a source pixel is identified:
    *   Replicate the source pixel's color to the pixel immediately to its right.
    *   Replicate the source pixel's color to the pixel in the bottom-right corner of the grid.
3. If no changes are made, keep the grid unchanged.
"""

import numpy as np

def find_source_pixel(grid):
    # find the non-white pixels
    non_white_pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                non_white_pixels.append((r, c, grid[r, c]))

    # if only one, return its coords and color, otherwise None
    if len(non_white_pixels) == 1:
        return non_white_pixels[0]
    else:
        return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # find source
    source_pixel = find_source_pixel(input_grid)

    # if source, replicate
    if source_pixel:
        row, col, color = source_pixel

        # replicate to the right, check for bounds
        if col + 1 < cols:
            output_grid[row, col + 1] = color

        # replicate to the bottom-right
        output_grid[rows - 1, cols - 1] = color

    return output_grid
```
