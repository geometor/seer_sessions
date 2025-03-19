"""
Identifies rectangular objects in the input grid and transforms them into hollow rectangles, 
preserving their outer border and color.
"""

import numpy as np

def find_objects(grid):
    """
    Finds all contiguous rectangular regions of non-white pixels.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, object_coords):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        object_coords.append((r, c))
        dfs(r + 1, c, color, object_coords)
        dfs(r - 1, c, color, object_coords)
        dfs(r, c + 1, color, object_coords)
        dfs(r, c - 1, color, object_coords)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                object_coords = []
                dfs(r, c, grid[r, c], object_coords)
                # Check if the object is rectangular
                if object_coords:
                  min_r = min(coord[0] for coord in object_coords)
                  max_r = max(coord[0] for coord in object_coords)
                  min_c = min(coord[1] for coord in object_coords)
                  max_c = max(coord[1] for coord in object_coords)
                  
                  # verify that the object found represents a rectangle, otherwise its
                  # an irregular shape, so ignore.
                  is_rectangle = True
                  for i in range(min_r, max_r + 1):
                    for j in range(min_c, max_c + 1):
                      if (i,j) not in object_coords:
                        is_rectangle = False
                        break
                    if not is_rectangle:
                      break
                  if is_rectangle:
                      objects.append({
                        "color": grid[r, c],
                        "min_row": min_r,
                        "max_row": max_r,
                        "min_col": min_c,
                        "max_col": max_c,
                      })
    return objects

def transform(input_grid):
    """
    Transforms the input grid by hollowing out detected rectangular objects.
    """
    output_grid = np.copy(input_grid)
    objects = find_objects(input_grid)

    # Iterate through each detected object
    for obj in objects:
        # Hollow out the object, leaving a 1-pixel border
        for r in range(obj["min_row"], obj["max_row"] + 1):
            for c in range(obj["min_col"], obj["max_col"] + 1):
                if (r == obj["min_row"] or r == obj["max_row"] or
                    c == obj["min_col"] or c == obj["max_col"]):
                    continue  # Keep border pixel
                else:
                    output_grid[r, c] = 0  # Set inner pixels to background color (0)

    return output_grid