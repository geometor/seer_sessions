"""
The transformation rule involves identifying objects of different colors (azure, green, and red) and applying specific horizontal expansion rules to them. Azure objects are expanded based on their initial width: width 1 becomes 3, and width 2 becomes 5. Green objects have their width increased by 2. Red objects remain unchanged.
"""

import numpy as np

def find_objects(grid):
    """Finds distinct objects in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, color, obj_coords):
        """Depth-first search to find contiguous regions."""
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj_coords.append((r, c))
        dfs(r + 1, c, color, obj_coords)
        dfs(r - 1, c, color, obj_coords)
        dfs(r, c + 1, color, obj_coords)
        dfs(r, c - 1, color, obj_coords)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c] and grid[r, c] != 0:
                obj_coords = []
                dfs(r, c, grid[r, c], obj_coords)
                objects.append({
                    "color": grid[r, c],
                    "coords": obj_coords,
                })
    return objects

def transform(input_grid):
    """Transforms the input grid according to the replication rules."""
    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Determine the maximum expansion needed
    max_expansion = 0
    for obj in objects:
      initial_width = max(c[1] for c in obj["coords"]) - min(c[1] for c in obj["coords"]) + 1

      if obj["color"] == 8: # Azure
        if initial_width == 1:
            expansion = 3
        elif initial_width == 2:
            expansion = 5
        else:
            expansion = initial_width #should not occur, keep width
        max_expansion = max(max_expansion, min(input_grid.shape[1] -1 , min(c[1] for c in obj["coords"]) + expansion -1))

      elif obj["color"] == 3: # Green

        expansion = initial_width + 2
        max_expansion = max(max_expansion,min(input_grid.shape[1] -1 , min(c[1] for c in obj["coords"]) + expansion - 1) )
      else:
          max_expansion = max(max_expansion, input_grid.shape[1] -1)


    # Initialize output grid with appropriate dimensions
    output_grid = np.zeros((input_grid.shape[0], max(input_grid.shape[1],max_expansion + 1)), dtype=int)


    for obj in objects:
        min_r = min(c[0] for c in obj["coords"])
        min_c = min(c[1] for c in obj["coords"])
        initial_width = max(c[1] for c in obj["coords"]) - min_c + 1

        if obj["color"] == 8:  # Azure
            # Replicate horizontally based on initial width
            if initial_width == 1:
                total_width = 3
            elif initial_width == 2:
                total_width = 5
            else:
                total_width = initial_width # Should not happen
            for r in range(min_r, max(c[0] for c in obj["coords"])+1):
              for c in range(min_c,min_c + total_width):
                  if c < output_grid.shape[1]:
                      output_grid[r,c] = obj["color"]


        elif obj["color"] == 3:  # Green
            # Replicate horizontally based on initial width

            total_width = initial_width + 2

            for r in range(min_r,max(c[0] for c in obj["coords"])+1):
                for c in range(min_c, min_c + total_width):
                  if c < output_grid.shape[1]:
                      output_grid[r,c] = obj["color"]

        elif obj["color"] == 2:  # Red
            # Copy the object without changes
            for r, c in obj["coords"]:
                if c < output_grid.shape[1]:
                  output_grid[r, c] = obj["color"]


    return output_grid