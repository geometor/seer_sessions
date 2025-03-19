"""
The task is to isolate a specific colored rectangular object from a grid containing multiple objects of different colors. The output grid consistently represents a single rectangle, and *not* the largest.
"""

import numpy as np

def get_objects(grid):
    """
    Identifies and extracts all rectangular objects within the grid.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, object_coords):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        object_coords.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, object_coords)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != 0:
                object_coords = []
                dfs(r, c, grid[r, c], object_coords)
                if object_coords:
                    #find top left and bottom right
                    min_r = min(coord[0] for coord in object_coords)
                    min_c = min(coord[1] for coord in object_coords)
                    max_r = max(coord[0] for coord in object_coords)
                    max_c = max(coord[1] for coord in object_coords)
                    
                    objects.append({
                        'color': grid[r, c],
                        'top_left': (min_r, min_c),
                        'height': max_r - min_r + 1,
                        'width' : max_c - min_c + 1,
                        'coords': object_coords
                    })
    return objects

def transform(input_grid):
    """
    Transforms the input grid by extracting a specific colored rectangle.
    """
    # Convert input grid to numpy array
    grid = np.array(input_grid)

    # Get all objects in the grid
    objects = get_objects(grid)
    
    # Find a object, which will be the target
    # select the first object as the output

    if len(objects) > 0:
      target_object = objects[-1]

      # Create output grid
      output_grid = np.full((target_object['height'], target_object['width']), target_object['color'], dtype=int)
      return output_grid.tolist()
    else:
       return []