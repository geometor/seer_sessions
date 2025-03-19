# 44f52bb0 • 002 • example_6 • investigate_coder

---
```python
"""
1.  **Count Contiguous Red Regions:** Examine the input grid. Identify distinct, contiguous regions of red (2) pixels.  Pixels are considered part of the same region if they are adjacent horizontally or vertically, but not diagonally.

2. **Determine color**:
    - If there is one contiguous red area output a blue (1)
    - If there are two, output an orange (7).
    - If there are three, output a blue (1).
    - If there are four, output a blue (1).

Essentially output 1 if the number of contiguous red regions is 1,3, or 4. Output 7 if the number of contiguous red regions is 2.
"""

import numpy as np

def count_contiguous_regions(grid, color):
    """Counts contiguous regions of a specified color in a grid."""
    visited = np.zeros_like(grid, dtype=bool)
    count = 0

    def dfs(row, col):
        """Depth-first search to explore a contiguous region."""
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        # Explore adjacent cells (up, down, left, right)
        dfs(row + 1, col)
        dfs(row - 1, col)
        dfs(row, col + 1)
        dfs(row, col - 1)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                dfs(row, col)
                count += 1
    return count

def transform(input_grid):
    """Transforms the input grid to output grid based on number of contiguous red pixels"""
    # Count contiguous red regions
    red_regions_count = count_contiguous_regions(np.array(input_grid), 2)

    # Determine output color based on the count
    if red_regions_count in (1, 3, 4):
      output_color = 1
    elif red_regions_count == 2:
      output_color = 7
    else: # handles 0 case
        output_color = 1


    # Create the 1x1 output grid
    output_grid = [[output_color]]

    return output_grid
```
