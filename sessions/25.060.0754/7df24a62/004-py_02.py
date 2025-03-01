"""
The transformation involves copying static yellow shapes. The blue shape overlapping the yellow shape are then copied to a different area, replacing the yellow.
"""

import numpy as np

def find_objects(grid, color):
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, obj):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj.append((r, c))
        dfs(r + 1, c, obj)
        dfs(r - 1, c, obj)
        dfs(r, c + 1, obj)
        dfs(r, c - 1, obj)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and not visited[r, c]:
                obj = []
                dfs(r, c, obj)
                objects.append(obj)
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find blue and yellow objects
    blue_objects = find_objects(input_grid, 1)
    yellow_objects = find_objects(input_grid, 4)
    
    # combine all blue objects into one object for easier handling
    blue_object = []
    for obj in blue_objects:
        blue_object.extend(obj)

    # Copy static yellow pixels
    for yellow_obj in yellow_objects:
      for r,c in yellow_obj:
        is_overlapping = False
        for br, bc in blue_object:
          if r == br and c == bc:
            is_overlapping = True
            break
        if not is_overlapping:
            output_grid[r, c] = 4
    

    # Find overlapping pixels between blue and yellow
    overlapping_pixels = []
    for r, c in blue_object:
        if input_grid[r, c] == 1:  # Ensure it's blue
            for yellow_obj in yellow_objects:
                for yr, yc in yellow_obj:
                  if r == yr and c == yc:
                    overlapping_pixels.append((r,c))
                    break

    # Calculate center offset for the bottom
    if overlapping_pixels:
        min_r = min(r for r, c in overlapping_pixels)
        max_r = max(r for r, c in overlapping_pixels)
        
        height = max_r - min_r + 1
        
        
        bottom_center_row = input_grid.shape[0] - (height+1)

        row_offset = bottom_center_row - min_r


    # Move overlapping blue pixels, replacing the yellow
    for r, c in overlapping_pixels:

            new_r = r + row_offset
            output_grid[new_r, c] = 1


    return output_grid