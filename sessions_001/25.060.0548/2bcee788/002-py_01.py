"""
1.  **Identify Objects:** Find all contiguous regions (objects) of non-zero pixels in the input grid.
2.  **Determine Dominant Color:** within each object, find one of the existing colors.
3.  **Fill:** If there is a dominant color within an object, fill the shape to remove all pixels not of the dominant color.
4. **Create background:** create a grid the same size as the input, color everything green (3).
5.  **Overlay Shape:** set the pixels of the changed object in the background grid, replacing the background color.
"""

import numpy as np

def find_objects(grid):
    """Find contiguous regions of non-zero pixels."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, current_object,color):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        dfs(r + 1, c, current_object, color)
        dfs(r - 1, c, current_object, color)
        dfs(r, c + 1, current_object, color)
        dfs(r, c - 1, current_object, color)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_object = []
                color = grid[r,c]
                dfs(r, c, current_object, color)
                objects.append((current_object,color))

    return objects



def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.full((rows, cols), 3)  # Initialize with green background

    objects = find_objects(input_grid)

    for obj_pixels,color in objects:
      # find the bounding box
      min_r = min(obj_pixels, key=lambda x:x[0])[0]
      max_r = max(obj_pixels, key=lambda x:x[0])[0]
      min_c = min(obj_pixels, key=lambda x:x[1])[1]
      max_c = max(obj_pixels, key=lambda x:x[1])[1]

      # choose a dominant color
      dominant_color = 0
      color_counts = {}
      for r,c in obj_pixels:
        pixel_color = input_grid[r,c]
        if pixel_color not in color_counts:
          color_counts[pixel_color] = 0
        color_counts[pixel_color] += 1
      max_count = 0
      for color in color_counts:
          if color_counts[color] > max_count:
            max_count=color_counts[color]
            dominant_color = color
        

      # change all pixels to dominant color
      for r,c in obj_pixels:
            output_grid[r,c] = dominant_color

    return output_grid.tolist()