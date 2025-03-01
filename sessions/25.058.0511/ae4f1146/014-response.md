# ae4f1146 • 014 • example_3 • investigate_coder

---
```python
"""
Extracts a subgrid from the input, where the subgrid is defined by the
location of blue pixels and their immediate azure neighbors. The rest of the
input grid is discarded.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the coordinates of all neighbors (including diagonals)."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append((i, j))
    return neighbors

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    blue_pixels = []

    # 1. Identify Target Pixels: Locate all 'blue' (1) pixels.
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 1:
                blue_pixels.append((r, c))

    if not blue_pixels:  # Handle cases with no blue pixels
        return []

    # 2. Define Extraction Region: Find bounding box and include azure neighbors.
    min_row = min(r for r, _ in blue_pixels)
    max_row = max(r for r, _ in blue_pixels)
    min_col = min(c for _, c in blue_pixels)
    max_col = max(c for _, c in blue_pixels)

    # expand the region for getting azure pixels
    target_pixels = set()
    for r in range(min_row,max_row+1):
       for c in range(min_col,max_col+1):
           if input_grid[r,c] == 1:
              target_pixels.add((r,c))
              for nr, nc in get_neighbors(input_grid, r, c):
                  if input_grid[nr, nc] == 8:
                     target_pixels.add((nr,nc))
    
    if not target_pixels:
        return []

    # 3. Extract Subgrid.
    min_row = min(r for r,_ in target_pixels)
    min_col = min(c for _,c in target_pixels)
    max_row = max(r for r,_ in target_pixels)
    max_col = max(c for _,c in target_pixels)

    output_grid = np.zeros((max_row - min_row + 1, max_col - min_col + 1), dtype=int)

    for r in range(min_row, max_row + 1):
      for c in range(min_col, max_col +1):
         if (r,c) in target_pixels:
            output_grid[r-min_row,c-min_col] = input_grid[r,c]


    return output_grid.tolist()
```
