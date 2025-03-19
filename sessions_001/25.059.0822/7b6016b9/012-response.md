# 7b6016b9 • 012 • refine_coder

---
```python
"""
1.  **Background Change:** Change all black (0) pixels in the input to green (3) in the output.
2.  **Identify Largest Enclosed Area:** Find the largest area enclosed by blue (1) pixels, regardless of whether it forms a perfect rectangle. It could be an irregular shape bounded by blue.
3.  **Fill Enclosed Area:** Change the color of the blue (1) pixels that form the boundary of the *largest* enclosed area to red (2).
4.  **Preserve Other Blues:** All other blue (1) pixels that are *not* part of the boundary of the largest enclosed area remain unchanged.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # 1. Change Background
    output_grid[output_grid == 0] = 3

    # Helper function to find connected components of a given color
    def get_connected_components(grid, color):
        visited = set()
        components = []

        def bfs(r, c):
            queue = deque([(r, c)])
            component = []
            while queue:
                row, col = queue.popleft()
                if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
                    continue
                visited.add((row, col))
                component.append((row, col))
                for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    queue.append((row + dr, col + dc))
            return component

        for r in range(grid.shape[0]):
            for c in range(grid.shape[1]):
                if grid[r, c] == color and (r, c) not in visited:
                    components.append(bfs(r, c))
        return components

    # Helper function to determine if a component encloses an area
    def is_enclosed(component, grid):
        # Check if any pixel in the component is on the edge of the grid
        for r, c in component:
            if r == 0 or r == grid.shape[0] - 1 or c == 0 or c == grid.shape[1] - 1:
                return False
        return True

    # 2. Identify Largest Enclosed Area
    blue_components = get_connected_components(input_grid, 1)
    enclosed_components = [comp for comp in blue_components if is_enclosed(comp, input_grid)]

   #find largest enclosed region
    largest_enclosed_area = []
    if len(enclosed_components) > 0:
      largest_enclosed_area = max(enclosed_components, key=len, default=[])

    # 3. Fill Enclosed Area (boundary only)
    if largest_enclosed_area:
        for r, c in largest_enclosed_area:
            output_grid[r, c] = 2

    # 4. Preserve Other Blues (already handled by only modifying the largest enclosed area)

    return output_grid
```
