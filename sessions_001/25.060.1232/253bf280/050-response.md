# 253bf280 • 050 • refine_coder

---
```python
"""
1.  **Identify Azure Objects:** Locate all azure (8) pixels in the input grid.  Consider contiguous azure pixels (horizontally or vertically adjacent) as a single object.

2.  **Expand Each Object:** For *each* identified azure object:
    *   Expand by adding a single green pixel to each open side.
    *   An open side exists if the adjacent cell is not azure or green, AND it is within grid bounds.
    * An azure object may contain 1 or more pixels.

3.  **Preserve Azure:** Maintain all existing azure pixels in their original locations, unchanged.

4.  **Maintain Zeros:** The white pixels remain as they are.
"""

import numpy as np

def find_azure_objects(grid):
    """Finds contiguous azure objects in the grid."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_object):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != 8:
            return
        visited[r, c] = True
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 8 and not visited[r, c]:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find azure objects.
    azure_objects = find_azure_objects(input_grid)

    # Expand each object.
    for obj in azure_objects:
        for row, col in obj:
            # Check and place green pixel above.
            if row > 0 and output_grid[row-1, col] != 3 and output_grid[row-1, col] != 8:
                output_grid[row-1, col] = 3
            # Check and place green pixel below.
            if row < rows - 1 and output_grid[row+1, col] != 3 and output_grid[row+1, col] != 8:
                output_grid[row+1, col] = 3
            # Check and place green pixel to the left.
            if col > 0 and output_grid[row, col-1] != 3 and output_grid[row, col-1] != 8:
                output_grid[row, col-1] = 3
            # Check and place green pixel to the right.
            if col < cols - 1 and output_grid[row, col+1] != 3 and output_grid[row, col+1] != 8:
                output_grid[row, col+1] = 3

    return output_grid
```

