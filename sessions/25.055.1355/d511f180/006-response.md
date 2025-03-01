# d511f180 • 006 • refine_coder

---
```python
"""
1.  **Global Swap:** Swap all pixels of color 8 (azure) with color 5 (gray) and all pixels of color 5 (gray) with color 8 (azure).
2.  **Conditional Magenta Swap:** Change any pixel of color 6 (magenta) to color 8 (azure) if *any* of its immediate neighbors (up, down, left, or right) is color 5 (gray).
3.  **Preservation:** All other pixels remain unchanged.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the neighbors of a cell."""
    rows, cols = grid.shape
    neighbors = {}
    if row > 0:
        neighbors["up"] = int(grid[row - 1, col])
    if row < rows - 1:
        neighbors["down"] = int(grid[row + 1, col])
    if col > 0:
        neighbors["left"] = int(grid[row, col - 1])
    if col < cols - 1:
        neighbors["right"] = int(grid[row, col + 1])
    return neighbors

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel of the input grid
    for r in range(rows):
        for c in range(cols):
            # Global Swap: Azure (8) and Gray (5)
            if input_grid[r, c] == 8:
                output_grid[r, c] = 5
            elif input_grid[r, c] == 5:
                output_grid[r, c] = 8
            # Conditional Magenta Swap
            elif input_grid[r, c] == 6:
                neighbors = get_neighbors(input_grid, r, c)
                if any(neighbor_color == 5 for neighbor_color in neighbors.values()):
                    output_grid[r, c] = 8

    return output_grid
```

