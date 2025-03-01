# 73251a56 • 018 • refine_coder

---
```python
"""
Removes white pixels (0) from within a specific colored shape, identified as a contiguous block of non-white, non-background pixels. The background color is determined as the most frequent color on the grid's edges.
"""

import numpy as np
from collections import Counter

def find_background_color(grid):
    """Finds the most frequent color on the edges of the grid."""
    edge_pixels = []
    rows, cols = grid.shape
    edge_pixels.extend(grid[0, :])  # Top row
    edge_pixels.extend(grid[rows - 1, :])  # Bottom row
    edge_pixels.extend(grid[:, 0])  # Left column
    edge_pixels.extend(grid[:, cols - 1])  # Right column
    color_counts = Counter(edge_pixels)
    return color_counts.most_common(1)[0][0]

def find_target_shape(grid, background_color):
    """Finds the contiguous non-white, non-background shape."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    shape_pixels = []

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, shape_color):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != shape_color:
            return
        visited[r, c] = True
        shape_pixels.append((r, c))
        # Check adjacent cells (up, down, left, right)
        dfs(r + 1, c, shape_color)
        dfs(r - 1, c, shape_color)
        dfs(r, c + 1, shape_color)
        dfs(r, c - 1, shape_color)


    for r in range(rows):
        for c in range(cols):
            if grid[r,c] != 0 and grid[r, c] != background_color and not visited[r,c]:
              first_shape_color = grid[r,c]
              dfs(r,c,first_shape_color)
              return shape_pixels # we only care about one shape for these examples

    return []

def transform(input_grid):
    """
    Removes white (0) pixels from within a specific colored shape.

    Args:
        input_grid: The input grid as a 2D numpy array.

    Returns:
        The transformed grid as a 2D numpy array.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # 1. Identify the background color.
    background_color = find_background_color(input_grid)

    # 2. Identify the target shape.
    shape_pixels = find_target_shape(input_grid, background_color)

    # 3. Remove white pixels inside the shape.
    for r, c in shape_pixels:
        if output_grid[r, c] == 0:
            output_grid[r, c] = 0  # Keep as 0

    return output_grid
```
