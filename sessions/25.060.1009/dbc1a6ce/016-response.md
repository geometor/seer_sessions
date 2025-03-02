# dbc1a6ce • 016 • example_3 • investigate_coder

---
```python
"""
1.  **Identify** all blue (1) pixels in the input grid.
2.  **For each** blue pixel:
    *   **Check directly adjacent cells:** If there is a blue pixel in a cardinal direction, change it into azure.
    *   If a cell is empty/white in a cardinal direction and not out-of-bounds of the image: Add a new azure (8) pixel to the directly adjacent cells (up, down, left, and right) of that current blue pixel. If the original blue pixel had *any* adjacent blue pixels, replace all original directly-adjacent blue pixels with an azure pixel.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell in the grid."""
    rows, cols = grid.shape
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < rows and 0 <= new_col < cols:
            neighbors.append((new_row, new_col))
    return neighbors

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find all blue pixels
    blue_pixels = [(r, c) for r in range(rows) for c in range(cols) if input_grid[r, c] == 1]

    for r, c in blue_pixels:
        neighbors = get_neighbors(input_grid, r, c)
        adjacent_blues = []
        for nr, nc in neighbors:
          if input_grid[nr,nc] == 1:
            adjacent_blues.append( (nr, nc) )

        if len(adjacent_blues) > 0:
            output_grid[r,c] = 8
            for nr, nc in adjacent_blues:
              output_grid[nr, nc] = 8
        else:
          #if no adjacent, then we add azure pixels
          for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = r + dr, c + dc
            if 0 <= new_row < rows and 0 <= new_col < cols and input_grid[new_row,new_col] == 0:
                output_grid[new_row, new_col] = 8
    return output_grid
```
