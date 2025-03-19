# 88a10436 • 016 • example_3 • investigate_coder

---
```python
"""
Remove the grey pixel and move a complex of red, green, and blue pixels to the top, while preserving the structure.
"""

import numpy as np

def find_cluster(grid, colors):
    # Find the bounding box of a cluster of specified colors.
    rows, cols = grid.shape
    min_row, min_col = rows, cols
    max_row, max_col = -1, -1

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] in colors:
                min_row = min(min_row, r)
                min_col = min(min_col, c)
                max_row = max(max_row, r)
                max_col = max(max_col, c)

    if max_row == -1: # no cluster found
      return None

    cluster = []
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            if grid[r,c] in colors:
              cluster.append( (r,c,grid[r,c]) )

    return (min_row, min_col), cluster

def transform(input_grid):
    # Initialize output grid with the same dimensions and default color (0).
    output_grid = np.zeros_like(input_grid)

    # Find the cluster of red, green, and blue pixels.
    cluster_colors = [1, 2, 3]  # Blue, Red, Green
    cluster_top_left, cluster = find_cluster(input_grid, cluster_colors)
    
    if cluster is None:
      return output_grid

    # Remove the gray pixel (5).
    rows, cols = input_grid.shape
    for r in range(rows):
      for c in range(cols):
        if input_grid[r,c] == 5:
          input_grid[r,c] = 0
          # print(f"removed 5 at {r} {c}")

    # Calculate the vertical shift needed.
    target_row = 1
    target_col = 3
    row_shift = target_row - cluster_top_left[0]
    col_shift = target_col - cluster_top_left[1]
    # print(f'shifting: row {row_shift} col {col_shift}')

    # Move the cluster in the output grid.
    for r,c,color in cluster:
      new_r = r + row_shift
      new_c = c + col_shift
      if 0 <= new_r < rows and 0 <= new_c < cols:  # Check boundaries
          output_grid[new_r, new_c] = color

    return output_grid
```
