# 681b3aeb • 014 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Colored Regions:** In the input grid, locate all distinct, contiguous regions of non-white (non-zero) pixels. In this specific example, find the blue (1) rectangle and the green (3) rectangle.

2.  **Determine Output Grid Size:** A 3x3 grid centered on green, and overlaps the corner of blue if the blue square was 2 up.

3. **Overlay.**: Blue occupies the top row and first column, green occupies the bottom row and the last column, overlapping will show whichever color was evaluated last.

4.  **Populate Output Grid:** Fill in the output grid. Blue overwrites the green in top left.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous regions of non-zero pixels."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_pixels):
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
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                obj_pixels = []
                dfs(row, col, grid[row, col], obj_pixels)
                objects.append(
                    {"color": grid[row, col], "pixels": obj_pixels}
                )
    return objects

def transform(input_grid):
    # Find the objects in the input grid
    objects = find_objects(input_grid)

    # Initialize the output grid as a 3x3 array of zeros
    output_grid = np.zeros((3, 3), dtype=int)

    # Iterate through the found objects
    for obj in objects:
        if obj["color"] == 1:  # Blue object
            # Blue occupies the top row and first column
            for i in range(3):
                output_grid[0, i] = 1  # Top row
                output_grid[i, 0] = 1 # First Column
        elif obj["color"] == 3:  # Green object
          for i in range(3):
            output_grid[2,i] = 3
            output_grid[i,2] = 3

    return output_grid
```
