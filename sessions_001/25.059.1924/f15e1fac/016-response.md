# f15e1fac • 016 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Azure Pixel Groups:** Find all groups of vertically contiguous azure (8) pixels in the input grid.
2.  **Horizontal Reflection:** For each distinct vertical group of azure pixels:
    *   If group in columns 0-3, extend to four 8s on the right.
    *   If group in columns 4-7, extend to four 8s on the left.
    *   If group in columns 8-11, extend to four 8s on the left.
3.  **Preserve Red Pixels:** Keep all red (2) pixels in their original positions in the output grid.
4. **Background:** All other cells will remain white (0)
"""

import numpy as np

def find_vertical_groups(grid, color):
    """Finds vertically contiguous groups of a specified color."""
    rows, cols = grid.shape
    groups = []
    visited = np.zeros((rows, cols), dtype=bool)

    def dfs(row, col, current_group):
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_group.append((row, col))
        dfs(row + 1, col, current_group)  # Check only downwards

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                group = []
                dfs(r, c, group)
                groups.append((group,c//4)) #add section to group
    return groups

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find azure pixel groups
    azure_groups = find_vertical_groups(input_grid, 8)

    # Reflect azure pixels horizontally
    for group, section in azure_groups:
        for row, col in group:
            if section == 0: #columns 0-3
              for i in range(4):
                output_grid[row,col+i]=8
            if section == 1: #columns 4-7
              for i in range(4):
                output_grid[row,col-i]=8
            if section == 2: #columns 8-11
              for i in range(4):
                output_grid[row,col-i]=8

    return output_grid.tolist()
```
