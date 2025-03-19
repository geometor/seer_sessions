# 11852cab • 014 • refine_coder

---
```python
"""
1.  **Identify Red Pixels:** Locate all red pixels (value 2) in the input grid.

2.  **Group Adjacent Red Pixels:** Identify groups of adjacent red pixels. Adjacency includes both horizontal and vertical neighbors. Diagonal pixels are *not* considered adjacent for the purpose of forming groups.

3.  **Expand Red Groups:** For each group of adjacent red pixels:
    *   **Extend Left:** Add one red pixel to the left of the leftmost pixel(s) in the group, if the extension is within the grid boundaries.
    *   **Extend Right:** Add one red pixel to the right of the rightmost pixel(s) in the group, if within bounds.
    *   **Extend Up:** Add one red pixel above the topmost pixel(s) in the group, if within bounds.
    *   **Extend Down:** Add one red pixel below the bottommost pixel(s) in the group, if within bounds.

4.  **Preserve Other Pixels:** Pixels that are not part of any expanded red group remain unchanged.

5. **No Red Pixels**: If the input array contains no red pixels, the output should be identical to the input.
"""

import numpy as np

def get_adjacent_pixels(grid, row, col):
    """Gets the valid adjacent pixels (up, down, left, right) of a given pixel."""
    rows, cols = grid.shape
    adjacent = []
    if row > 0:
        adjacent.append((row - 1, col))  # Up
    if row < rows - 1:
        adjacent.append((row + 1, col))  # Down
    if col > 0:
        adjacent.append((row, col - 1))  # Left
    if col < cols - 1:
        adjacent.append((row, col + 1))  # Right
    return adjacent

def group_red_pixels(grid):
    """Groups contiguously adjacent red pixels using Depth-First Search (DFS)."""
    rows, cols = grid.shape
    visited = set()
    groups = []

    def dfs(row, col, current_group):
        if (row, col) in visited or grid[row, col] != 2:
            return
        visited.add((row, col))
        current_group.append((row, col))
        for r, c in get_adjacent_pixels(grid, row, col):
            dfs(r, c, current_group)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 2 and (r, c) not in visited:
                current_group = []
                dfs(r, c, current_group)
                groups.append(current_group)
    return groups

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find and group red pixels
    red_groups = group_red_pixels(input_grid)

    # If no red pixels, return original grid
    if not red_groups:
        return output_grid

    # Expand red groups
    for group in red_groups:
        # Collect all pixels to expand to
        expansion_pixels = set()
        for r, c in group:
            for ar, ac in get_adjacent_pixels(input_grid, r, c):
                expansion_pixels.add((ar,ac))

        # expand to red
        for r, c in expansion_pixels:
          output_grid[r,c] = 2
          
    return output_grid
```
