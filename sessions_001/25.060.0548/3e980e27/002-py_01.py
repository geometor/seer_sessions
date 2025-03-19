"""
The transformation rule identifies contiguous shapes of non-zero colored pixels in the input grid.
For each shape, it creates a copy and swaps places with the first object.
Finally, it outputs the grid with the replicated and translated shapes.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects (shapes) in the grid."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_object = []
                dfs(r, c, grid[r, c], current_object)
                objects.append((grid[r, c], current_object))
    return objects

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # Find objects in the input grid.
    objects = find_objects(input_grid)

    # if only one shape, return input
    if len(objects) <= 1:
        return input_grid.tolist()

    # Copy the original grid to output first
    for color, obj_pixels in objects:
          for r,c in obj_pixels:
            output_grid[r,c] = color

    # replicate and translate
    if len(objects) >= 2:

        obj1_color, obj1_pixels = objects[0]
        obj2_color, obj2_pixels = objects[1]


        # swap pixel locations
        for r, c in obj1_pixels:
          output_grid[r,c] = 0
        for r, c in obj2_pixels:
          output_grid[r,c] = 0

        for r, c in obj1_pixels:
            # find corresponding pixel in obj2, if its a single pixel
            if len(obj2_pixels) == 1:
              r2, c2 = obj2_pixels[0]
              output_grid[r2,c2] = obj1_color
            else:
              # find matching pixel from first object and move it to second object
              min_r1 = min(r for r, _ in obj1_pixels)
              min_c1 = min(c for _, c in obj1_pixels)
              min_r2 = min(r for r, _ in obj2_pixels)
              min_c2 = min(c for _, c in obj2_pixels)

              delta_r = r - min_r1
              delta_c = c - min_c1

              new_r = min_r2 + delta_r
              new_c = min_c2 + delta_c
              output_grid[new_r, new_c] = obj1_color


        for r, c in obj2_pixels:
            if len(obj1_pixels) == 1:
                r1,c1 = obj1_pixels[0]
                output_grid[r1,c1] = obj2_color
            else:
                # Find matching pixel and copy to object 1
                min_r1 = min(r for r, _ in obj1_pixels)
                min_c1 = min(c for _, c in obj1_pixels)
                min_r2 = min(r for r, _ in obj2_pixels)
                min_c2 = min(c for _, c in obj2_pixels)

                delta_r = r - min_r2
                delta_c = c - min_c2

                new_r = min_r1 + delta_r
                new_c = min_c1 + delta_c

                output_grid[new_r,new_c] = obj2_color
    
    # handle 3 objects
    if len(objects) == 3:
        obj3_color, obj3_pixels = objects[2]

        for r, c in obj3_pixels:
           output_grid[r,c] = 0 # reset to blank

        # place object 3 at end of object 2
        for r, c in obj3_pixels:
           output_grid[r - 1, c - len(obj3_pixels)] = obj3_color

    if len(objects) > 3:
        # copy remaining colors
        for i in range(3, len(objects)):
          obj_color, obj_pixels = objects[i]
          # add new colors
          for r,c in obj_pixels:
            output_grid[r,c] = obj_color

    return output_grid.tolist()