# 00d62c1b • 028 • refine_coder

---
```python
"""
1.  **Identify** all connected components of green (3) pixels in the input grid.
2.  **For each** green connected component:
    a.  **Determine** the bounding box of the component. The bounding box is the smallest rectangle (defined by its top-left and bottom-right corners) that completely encloses the green component.
    b. **Identify** all of the green pixels that would be contained within the extent of the bounding box.
    c.  **Change** the color of the internal green pixels within the bounding box to yellow (4).
3.  **Leave** all other pixels unchanged.
"""

import numpy as np

def get_connected_components(grid, color):
    """Finds connected components of a given color."""
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    def dfs(r, c, current_component):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        current_component.append((r, c))
        dfs(r + 1, c, current_component)
        dfs(r - 1, c, current_component)
        dfs(r, c + 1, current_component)
        dfs(r, c - 1, current_component)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and not visited[r, c]:
                current_component = []
                dfs(r, c, current_component)
                components.append(current_component)
    return components

def get_bounding_box(component):
    """Calculates the bounding box of a component."""
    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')
    for r, c in component:
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)
    return (min_r, min_c), (max_r, max_c)

def transform(input_grid):
    """Fills the internal regions of green areas with yellow."""
    output_grid = np.copy(input_grid)
    green_components = get_connected_components(input_grid, 3)

    for component in green_components:
        # Determine the bounding box
        (min_r, min_c), (max_r, max_c) = get_bounding_box(component)

        # Iterate through the bounding box and change green pixels to yellow
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                if output_grid[r,c] == 3:
                    output_grid[r, c] = 4

    return output_grid
```
