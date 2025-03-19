# 29ec7d0e • 004 • example_1 • investigate_coder

---
```python
"""
1. Identify Zeroes: Locate all cells in the input grid with the value '0' (representing white).
2. Remove Zeroes and propagate removal: delete all cells with value '0'. Delete any cells immediately above or below a cell with '0'.
3. The remaining cells stay the same: Any cells that are not removed by the previous steps are not changed and keep their location and value.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid by removing 0-value cells and propagating the removal vertically."""

    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 1. Identify Zeroes and mark for removal.
    zero_positions = []
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 0:
                zero_positions.append((r, c))

    # 2. Remove Zeroes and Propagate Removal Vertically.
    for r, c in zero_positions:
        #remove the 0 cell
        output_grid[r,c] = -1 #mark to be removed

        # Propagate upwards
        for up_r in range(r - 1, -1, -1):
            output_grid[up_r, c] = -1

        # Propagate downwards
        for down_r in range(r + 1, rows):
            output_grid[down_r, c] = -1

    #remove the marked cells
    for r in range(rows):
      for c in range(cols):
        if output_grid[r,c] == -1:
          #find the most frequent value in input.
          unique, counts = np.unique(input_grid, return_counts=True)
          most_frequent_value = unique[np.argmax(counts)]
          #replace with the most frequent value
          output_grid[r,c] = most_frequent_value


    return output_grid
```
