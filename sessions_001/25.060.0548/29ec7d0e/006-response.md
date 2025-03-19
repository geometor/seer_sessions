# 29ec7d0e • 006 • refine_coder

---
```python
"""
1.  Identify Zeroes: Locate all cells in the input grid with the value '0' (representing white).
2.  Remove Zeroes and Vertically Connected Cells: Delete all cells with the value '0'. Also, delete any cells immediately above or below a cell with value '0'. Continue this vertical propagation until a non-zero cell (or the edge of the grid) is encountered.
3. Expose the Background: The removal of the cells effectively exposes the "background."
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid by removing 0-value cells and propagating the removal vertically, exposing the background."""

    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    background_color = 1 #from observation of outputs, background is always blue

    # 1. Identify Zeroes and mark for removal.
    zero_positions = []
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 0:
                zero_positions.append((r, c))

    # 2. Remove Zeroes and Propagate Removal Vertically.
    for r, c in zero_positions:
        #remove the 0 cell
        output_grid[r,c] = background_color #expose background

        # Propagate upwards
        for up_r in range(r - 1, -1, -1):
            if output_grid[up_r,c] == 0:
                output_grid[up_r, c] = background_color
            else:
                output_grid[up_r, c] = background_color
                break #stop on hitting non-zero

        # Propagate downwards
        for down_r in range(r + 1, rows):
            if output_grid[down_r,c] == 0:
                output_grid[down_r, c] = background_color
            else:
                output_grid[down_r, c] = background_color
                break


    return output_grid
```

