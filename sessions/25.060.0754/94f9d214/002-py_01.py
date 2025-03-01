"""
1. **Identify Green Regions:** Locate all contiguous regions (connected components) of green (3) pixels within the input grid.

2. **Bounding Box:** For each green region, determine its bounding box. A bounding box is defined here as a minimal rectangle aligned to grid axes that encloses the component.

3. **Translate and Scale:** Each green pixel is translated to one red pixel in output grid.
    - Take the set of the coordinates of the top left corner of the minimal rectangle bounding the green regions,
    - Find the lowest x and y coordinates, consider this the top left corner of the red area.
    - Do the same with bottom right corners of green rectangles. Consider this bottom right corner of the red area.

4. **Output Grid Creation:** Create an output grid with dimensions 4x4. Fill it entirely with white (0) pixels.

5. **Fill Red Pixels:** Within the output grid, place the red pixels according to the bounding boxes, computed in step 3.
"""

import numpy as np

def find_objects(grid, color):
    """Finds connected components of a specific color in a grid."""
    visited = set()
    objects = []

    def dfs(r, c, current_object):
        if (r, c) in visited or r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def bounding_box(object_pixels):
    """Calculates the bounding box of a set of pixels."""
    if not object_pixels:
        return None
    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')
    for r, c in object_pixels:
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)
    return (min_r, min_c), (max_r, max_c)

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # 1. Identify Green Regions
    green_objects = find_objects(input_grid, 3)

    # 2. & 3. Bounding Box and Translate
    top_left_corners = []
    bottom_right_corners = []
    for obj in green_objects:
      bb = bounding_box(obj)
      if bb:
        top_left_corners.append(bb[0])
        bottom_right_corners.append(bb[1])

    # Find min and max coordinates for translation
    min_r = min([r for r, c in top_left_corners], default=float('inf'))
    min_c = min([c for r, c in top_left_corners], default=float('inf'))

    max_r = max([r for r, c in bottom_right_corners], default=float('-inf'))
    max_c = max([c for r, c in bottom_right_corners], default=float('-inf'))

    # 4. Output Grid Creation
    output_grid = np.zeros((4, 4), dtype=int)

    # 5. Fill Red Pixels (Translate and Scale)
    if min_r != float('inf'):
        # Calculate translated coordinates within the 4x4 output grid.
        out_min_r = int(((min_r-min_r) / (max(1,input_grid.shape[0]-1))) * 3) if input_grid.shape[0] > 1 else 0
        out_min_c = int(((min_c-min_c)/ (max(1,input_grid.shape[1]-1)))* 3)  if input_grid.shape[1] > 1 else 0

        out_max_r = int(((max_r-min_r)/ (max(1, input_grid.shape[0]-1))) * 3) if input_grid.shape[0] > 1 else 0
        out_max_c = int(((max_c-min_c) / (max(1, input_grid.shape[1]-1)))* 3) if input_grid.shape[1] > 1 else 0
        
        # Ensure coordinates are within bounds
        out_min_r = max(0, min(3, out_min_r))
        out_min_c = max(0, min(3, out_min_c))
        out_max_r = max(0, min(3, out_max_r))
        out_max_c = max(0, min(3, out_max_c))

        for r in range(out_min_r, out_max_r + 1):
          for c in range(out_min_c, out_max_c+1):
            output_grid[r,c] = 2


    return output_grid