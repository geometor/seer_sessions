"""
1.  **Identify Objects:** Find all distinct, connected components (objects) in the input grid. In this case green (3) and orange (7).
2.  **Determine Output Grid:** the output is a 3x3 grid
3. **Place Objects:**
    *   The first column will contain all the green pixels vertically stacked.
    *   The third column will contain all the orange pixels vertically stacked
    *   The second column will be the first column stacked on the second
"""

import numpy as np

def get_objects(grid):
    """Finds distinct connected components in the grid."""
    objects = {}
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, color, obj_id):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        objects[obj_id].append((r, c))
        dfs(r + 1, c, color, obj_id)
        dfs(r - 1, c, color, obj_id)
        dfs(r, c + 1, color, obj_id)
        dfs(r, c - 1, color, obj_id)

    obj_id = 0
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c] and grid[r, c] != 0:
                objects[obj_id] = []
                dfs(r, c, grid[r, c], obj_id)
                obj_id += 1
    return objects
def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Find connected components
    objects = get_objects(input_grid)
    
    # place objects into output grid
    for obj_id, pixels in objects.items():
      color = input_grid[pixels[0]]
      if color == 3: #green
        for i in range(len(pixels)):
          if i < 3:
            output_grid[i,0] = 3
      elif color == 7:
        for i in range(len(pixels)):
          if i < 3:
            output_grid[i,2] = 7
    
    output_grid[0:3, 1] = output_grid[0:3, 2]
    output_grid[0:2, 1] = output_grid[0:2, 0]

    return output_grid