"""
1.  **Yellow Transformation:** All yellow (4) pixels in the input grid are transformed to gray (5) pixels in the output grid.

2.  **Red and Green Preservation:** If there are distinct rectangular regions of Red (2) *and* Green (3) in the input, do *not* change their colors.

3.  **Red and Green Transformation (Conditional):** If either Red (2) or Green (3) are absent, or are not separated, then transform all instances of both of those colors to White (0).
"""

import numpy as np

def find_objects(grid):
    """Finds distinct rectangular regions of the same color."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def is_valid(x, y):
        return 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]

    def dfs(x, y, color, object_coords):
        if not is_valid(x, y) or visited[x, y] or grid[x, y] != color:
            return
        visited[x, y] = True
        object_coords.append((x, y))
        dfs(x + 1, y, color, object_coords)
        dfs(x - 1, y, color, object_coords)
        dfs(x, y + 1, color, object_coords)
        dfs(x, y - 1, color, object_coords)

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if not visited[i, j]:
                color = grid[i, j]
                object_coords = []
                dfs(i, j, color, object_coords)
                if object_coords:
                    # Check if it forms a rectangle
                    xs, ys = zip(*object_coords)
                    min_x, max_x = min(xs), max(xs)
                    min_y, max_y = min(ys), max(ys)
                    if len(object_coords) == (max_x - min_x + 1) * (max_y - min_y + 1):
                      objects.append({"color": color, "coords": object_coords})
    return objects

def transform(input_grid):
    """Transforms the input grid according to the specified color mapping."""
    output_grid = np.copy(input_grid)
    objects = find_objects(input_grid)
    
    # Extract colors and their counts from the objects.  Much more reliable
    # than a raw count.
    colors = [obj['color'] for obj in objects]
    color_counts = {}
    for c in colors:
        color_counts[c] = color_counts.get(c,0) + 1
    
    # Yellow Transformation
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if input_grid[i, j] == 4:
                output_grid[i, j] = 5

    # Red and Green Transformation
    red_present = 2 in color_counts
    green_present = 3 in color_counts
    
    separate_regions = True # assume true unless we find evidence below

    if red_present and green_present:
        # check for overlap

        red_coords = []
        green_coords = []

        for obj in objects:
          if obj['color'] == 2:
            red_coords.extend(obj['coords'])
          if obj['color'] == 3:
            green_coords.extend(obj['coords'])
        
        # brute force check if red and green share the same coordinates
        for r_coord in red_coords:
            for g_coord in green_coords:
                if r_coord == g_coord:
                    separate_regions = False
                    break

    if red_present or green_present:
        if not (red_present and green_present and separate_regions):
          for i in range(input_grid.shape[0]):
              for j in range(input_grid.shape[1]):
                  if input_grid[i,j] == 2 or input_grid[i,j] == 3:
                      output_grid[i,j] = 0

    return output_grid