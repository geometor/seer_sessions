# 6773b310 • 024 • refine_coder

---
```python
"""
Identifies the largest connected component of azure (8) pixels in the input grid and represents it as a single blue (1) pixel in the center of a 3x3 output grid. All other pixels in the output grid are set to black (0). Ignores magenta (6) pixels.
"""

import numpy as np

def find_largest_connected_component(grid, color):
    """
    Finds the largest connected component of a given color in the grid.
    Uses Depth-First Search (DFS).
    """
    visited = set()
    max_component = []

    def dfs(row, col, current_component):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return

        visited.add((row, col))
        current_component.append((row, col))

        # Explore adjacent cells (up, down, left, right)
        dfs(row + 1, col, current_component)
        dfs(row - 1, col, current_component)
        dfs(row, col + 1, current_component)
        dfs(row, col - 1, current_component)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and (row, col) not in visited:
                current_component = []
                dfs(row, col, current_component)
                if len(current_component) > len(max_component):
                    max_component = current_component
    return max_component

def transform(input_grid):
    # Initialize output grid as all black (0)
    output_grid = np.zeros((3, 3), dtype=int)

    # Find the largest connected component of azure (8) pixels
    input_grid = np.array(input_grid)
    largest_component = find_largest_connected_component(input_grid, 8)

    # If an azure component is found, set the center of the output grid to blue (1)
    if largest_component:
        output_grid[1, 1] = 1

    return output_grid.tolist()
```

