# 928ad970 • 005 • refine_coder

---
```python
"""
1.  **Identify Regions:** Find all contiguous regions of pixels with the same color. Consider pixels connected horizontally or vertically as part of the same region.
2. **Gray Regions:** Gray (color 5) regions do not change.
3.  **Blue Regions:** Expand each blue (color 1) region vertically by one pixel.
    *   For each pixel in the blue region, check the cells directly above and below.
    *   If an adjacent cell is background (color 0), change that cell to blue (color 1).
"""

import numpy as np

def get_regions(grid):
    """
    Identifies contiguous regions of the same color.
    Returns a dictionary of regions, where the key is the color and the value is a list of (row, col) tuples.
    """
    visited = set()
    regions = {}
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if (r, c) not in visited and color != 0:
                if color not in regions:
                    regions[color] = []
                stack = [(r, c)]
                visited.add((r, c))
                while stack:
                    curr_r, curr_c = stack.pop()
                    regions[color].append((curr_r, curr_c))

                    neighbors = []
                    if curr_r > 0: neighbors.append((curr_r - 1, curr_c))
                    if curr_r < rows - 1: neighbors.append((curr_r + 1, curr_c))
                    if curr_c > 0: neighbors.append((curr_r, curr_c - 1))
                    if curr_c < cols - 1: neighbors.append((curr_r, curr_c + 1))

                    for nr, nc in neighbors:
                        if (nr, nc) not in visited and grid[nr, nc] == color:
                            stack.append((nr, nc))
                            visited.add((nr, nc))
    return regions

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Identify Regions
    regions = get_regions(input_grid)

    # Gray regions do not change (implicitly handled by copying the input grid)

    # Expand blue regions vertically
    if 1 in regions:  # Check if blue exists
      for r, c in regions[1]:
          # Check above
          if r > 0 and output_grid[r - 1, c] == 0:
              output_grid[r - 1, c] = 1
          # Check below
          if r < rows - 1 and output_grid[r + 1, c] == 0:
              output_grid[r + 1, c] = 1

    return output_grid.tolist()
```
