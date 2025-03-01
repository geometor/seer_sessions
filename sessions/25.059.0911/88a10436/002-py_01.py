"""
The transformation identifies multi-pixel colored objects within the input grid.
It also finds a uniquely colored single pixel object, and moves a copy of the
source object to that location in the output.
"""

import numpy as np
from collections import Counter

def find_objects(grid):
    # Find all contiguous colored objects (connected components).
    objects = []
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def dfs(r, c, color, obj):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != color:
            return
        visited.add((r, c))
        obj.append((r, c))
        dfs(r + 1, c, color, obj)
        dfs(r - 1, c, color, obj)
        dfs(r, c + 1, color, obj)
        dfs(r, c - 1, color, obj)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                obj = []
                color = grid[r][c]
                dfs(r, c, color, obj)
                if obj:
                    objects.append((color, obj))
    return objects

def find_target_location(grid, objects):
     # Find the location of single-pixel object with unique color.
    color_counts = Counter()
    pixel_locations = {}

    rows, cols = len(grid), len(grid[0])
    for r in range(rows):
        for c in range(cols):
            color_counts[grid[r][c]] += 1
            pixel_locations[grid[r][c]] = (r,c)

    for color, count in color_counts.items():
        is_object = False
        for object_color, obj_pixels in objects:
          if color == object_color:
            is_object = True
        if count == 1 and not is_object:
          return pixel_locations[color]

    return None


def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    # Convert input grid to numpy array
    grid = np.array(input_grid)

    # Find objects
    objects = find_objects(grid)
    # print(f"objects {objects}")

    # Find target location
    target_location = find_target_location(grid, objects)
    # print(f"target {target_location}")

    # Initialize output_grid as copy of the grid
    output_grid = np.copy(grid)

    # skip if no target
    if not target_location:
      return output_grid.tolist()
      
    # Find object to move
    # Identify Source Objects: select multi-pixel colored objects
    source_objects = []
    for color, obj_pixels in objects:
      if len(obj_pixels) > 1:
        source_objects.append((color, obj_pixels))

    # print(f"source: {source_objects}")
    
    # skip if not source
    if len(source_objects) == 0:
        return output_grid.tolist()

    for (source_color, source_pixels) in source_objects:
        # Translate object: Center of selected object becomes target location.

        # Compute centroid of source object
        source_rows, source_cols = zip(*source_pixels)
        source_centroid_r = int(np.mean(source_rows))
        source_centroid_c = int(np.mean(source_cols))

        # Calculate translation offset
        offset_r = target_location[0] - source_centroid_r
        offset_c = target_location[1] - source_centroid_c
        
        # print(f"offset: {(offset_r, offset_c)}")

        # Create a translated copy of the object in the output grid.
        for r, c in source_pixels:
            new_r, new_c = r + offset_r, c + offset_c
            # Ensure indices are within bounds
            if 0 <= new_r < output_grid.shape[0] and 0 <= new_c < output_grid.shape[1]:
              output_grid[new_r, new_c] = source_color

    return output_grid.tolist()