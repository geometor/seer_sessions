# e8593010 • 007 • refine_coder

---
```python
"""
1. Preserve the Gray Rectangle: The gray (5) rectangle in the input grid is copied directly to the output grid without modification.
2. Create a Blue Frame: A 3x3 L-shaped (or filled square) frame of blue (1) pixels is created in the top-left corner of the output grid, regardless of the original colors in the input grid.
3. Create a Red Frame: A 3x3 L-shaped (or filled square) frames of red(2) pixels are created in the top-right and bottom-right corners of the output grid.
4. Create a Green Frame: Excluding any corner pixels, a one-pixel-wide frame of green(3) pixels along the edges is created.
"""

import numpy as np

def get_rectangle(grid, color):
    # find top-left and bottom-right coordinates
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None
    min_row, min_col = np.min(rows), np.min(cols)
    max_row, max_col = np.max(rows), np.max(cols)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 1. Preserve the Gray Rectangle
    # (This is already handled by copying the input_grid to output_grid)

    # 2. Create a Blue Frame (top-left corner)
    output_grid[:3, :3] = 1

    # 3. Create a Red Frame (top-right and bottom-right corners)
    output_grid[:3, cols-3:] = 2
    output_grid[rows-3:, cols-3:] = 2


    # 4. Create Green Frame - all edges, excluding corners
    output_grid[0, 3:cols-3] = 3          # Top edge
    output_grid[rows-1, 3:cols-3] = 3   # Bottom edge
    output_grid[3:rows-3, 0] = 3          # Left edge
    output_grid[3:rows-3, cols-1] = 3   # Right edge



    return output_grid
```
