# 32597951 • 004 • example_1 • investigate_coder

---
```python
"""
Identify a contiguous region of azure (8) pixels. Within this region, change the color of some azure pixels to green (3), specifically to the immediate left, right, above and below a central 8.  All other pixels remain unchanged.
"""

import numpy as np

def find_contiguous_region(grid, color):
    # Find all pixels of the specified color.
    pixels = np.argwhere(grid == color)
    if len(pixels) == 0:
        return []

    # Initialize the region with the first pixel.
    region = [tuple(pixels[0])]
    queue = [tuple(pixels[0])]

    # Perform a breadth-first search to find all connected pixels.
    while queue:
        x, y = queue.pop(0)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] and
                grid[nx, ny] == color and (nx, ny) not in region):
                region.append((nx, ny))
                queue.append((nx, ny))
    return region

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)
    grid_height = output_grid.shape[0]
    grid_width = output_grid.shape[1]

    # Find the contiguous azure region.
    azure_region = find_contiguous_region(input_grid, 8)

    # Find a "central" azure pixel within the region, use (grid_height // 2, grid_width // 2) as reference.
    central_azure = None
    if (grid_height // 2, grid_width // 2) in azure_region:
       central_azure = (grid_height // 2, grid_width // 2)

    #if not in azure_region, then walk the azure_region to fine the one closest.
    if not central_azure:
      min_dist = 1000
      for x,y in azure_region:
          dist = abs(x - grid_height//2) + abs(y - grid_width//2)
          if dist < min_dist:
              min_dist = dist
              central_azure = (x,y)


    # Change some azure pixels to green based on adjacency to the central azure.

    if central_azure:
      for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
          nx, ny = central_azure[0] + dx, central_azure[1] + dy
          if (0 <= nx < input_grid.shape[0] and 0 <= ny < input_grid.shape[1] and
                (nx,ny) in azure_region):
                output_grid[nx, ny] = 3


    return output_grid
```
