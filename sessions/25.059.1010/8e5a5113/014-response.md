# 8e5a5113 • 014 • refine_coder

---
```python
"""
The transformation identifies enclosed regions of non-white (non-zero) colors within the white (0) background and replaces the enclosed color with the color of another object within the same enclosed area.
"""

import numpy as np
from collections import Counter

def get_objects(grid):
    """
    Identifies contiguous regions of the same color (objects).
    Returns a dictionary where keys are object IDs and values are lists of (row, col) coordinates.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = {}
    object_id_counter = 0

    def dfs(r, c, color, object_id):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        objects[object_id].append((r, c))
        dfs(r + 1, c, color, object_id)
        dfs(r - 1, c, color, object_id)
        dfs(r, c + 1, color, object_id)
        dfs(r, c - 1, color, object_id)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c]:
                color = grid[r, c]
                object_id_counter += 1
                objects[object_id_counter] = []
                dfs(r, c, color, object_id_counter)
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    objects = get_objects(input_grid)

    # Find objects enclosed by background (0)
    enclosed_objects = {}
    for obj_id, pixels in objects.items():
        # Check if all neighbors of the object's pixels are either the same color or 0
        enclosed = True
        dominant_internal_color = None
        internal_colors = []
        for r, c in pixels:
            neighbors = []
            if r > 0: neighbors.append(input_grid[r-1, c])
            if r < rows - 1: neighbors.append(input_grid[r+1, c])
            if c > 0: neighbors.append(input_grid[r, c-1])
            if c < cols - 1: neighbors.append(input_grid[r, c+1])

            for neighbor_color in neighbors:
                if neighbor_color != 0 and neighbor_color != input_grid[r,c]:
                    enclosed = False
                    break
            if input_grid[r,c] != 0:
                internal_colors.append(input_grid[r,c])
            if not enclosed: break;
        
        if enclosed and len(internal_colors)>0:
            enclosed_objects[obj_id] = pixels

    # perform flood fill
    for obj_id, pixels in enclosed_objects.items():
      first_pixel = pixels[0]
      enclosed_color = input_grid[first_pixel]
      
      # find other colors in enclosing object
      other_colors = []
      for other_obj_id, other_pixels in objects.items():
        if other_obj_id != obj_id:
            first_other_pixel = other_pixels[0]
            if input_grid[first_other_pixel] != 0:
                is_inside = False
                for r, c in other_pixels:
                    is_inside = False
                    for er, ec in pixels:
                        neighbors = []
                        if er > 0: neighbors.append((er-1, ec))
                        if er < rows - 1: neighbors.append((er+1, ec))
                        if ec > 0: neighbors.append((er, ec-1))
                        if ec < cols - 1: neighbors.append((er, ec+1))
                        for nr, nc in neighbors:
                            if (nr,nc) == (r,c): 
                                is_inside = True
                                break
                        if is_inside: break
                    if is_inside: break

                if is_inside:
                  other_colors.append(input_grid[first_other_pixel]) # add one of the colors
      
      # replace this object with other_color if found
      if len(other_colors)>0:
          fill_color = other_colors[0]
          for r, c in pixels:
              output_grid[r,c] = fill_color

    return output_grid
```
