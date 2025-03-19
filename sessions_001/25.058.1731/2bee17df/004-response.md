# 2bee17df • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify Regions:** Locate the regions of red (2) pixels at the top right, azure (8) pixels on the left and bottom, and white (0) pixels in the rest of the grid.

2.  **Define Green Region Boundaries:**
    *   Find the inner most azure pixels, this can be done by checking pixels with azure value that has white pixel neighbor
    *   Starting on the 4th row from top and 4th column from left. Fill area with green until the 9th row and 9th column. There is an interruption.

3. Replace: All white pixels inside the rectangle will be green color, except those are next to red pixels.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Returns a list of neighbors (up, down, left, right) for a given cell."""
    neighbors = []
    rows, cols = grid.shape
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find inner azure pixels (adjacent to white)
    inner_azure_pixels = []
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 8:
                for nr, nc in get_neighbors(output_grid, r, c):
                    if output_grid[nr, nc] == 0:
                        inner_azure_pixels.append((r,c))
                        break

    # Define Green region, starts from (3,3), 1-indexed, so index is 3
    for r in range(3, 9):
      for c in range(3, 9):
        # skip replacement when adjcent to red pixels
        neighbor_red = False
        for neighbor_row, neighbor_col in get_neighbors(output_grid,r, c):
          if output_grid[neighbor_row, neighbor_col] == 2:
            neighbor_red = True
            break
        if not neighbor_red and output_grid[r,c] == 0:
          output_grid[r,c] = 3

    return output_grid
```
