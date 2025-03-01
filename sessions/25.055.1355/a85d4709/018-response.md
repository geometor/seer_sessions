# a85d4709 • 018 • refine_coder

---
```python
"""
1.  **Identify Objects:**  Group contiguous pixels of the same color into distinct objects.
2.  **Gray Object Center:** For each gray object, determine its geometric center.  If the object has an odd number of rows and columns, the center is a single pixel. If either dimension is even, there isn't a single center pixel; in such case gray pixels are always red.
3.  **Gray Transformation:**
    *   If a gray pixel is the center of a gray *object*, change it to yellow (4).
    *   If a gray pixel is part of a gray object, but *not* the center of the object, change it to red (2).
    * If the object has no single center, all gray pixels become red (2).
4.  **White Transformation:** Change all white (0) pixels to red (2).
"""

import numpy as np

def find_objects(grid):
    """
    Identifies contiguous objects of the same color in a grid.
    Returns a dictionary where keys are colors and values are lists of pixel coordinates.
    """
    objects = {}
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color):
        if (r, c) in visited or not (0 <= r < rows and 0 <= c < cols) or grid[r, c] != color:
            return []
        visited.add((r, c))
        object_pixels = [(r, c)]
        object_pixels.extend(dfs(r + 1, c, color))
        object_pixels.extend(dfs(r - 1, c, color))
        object_pixels.extend(dfs(r, c + 1, color))
        object_pixels.extend(dfs(r, c - 1, color))
        return object_pixels

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                color = grid[r, c]
                if color not in objects:
                    objects[color] = []
                objects[color].append(dfs(r, c, color))
    return objects

def find_object_center(object_pixels):
    """
    Calculates the geometric center of an object. Returns None if there is no single center pixel.
    """
    if not object_pixels:
        return None

    rows = [r for r, _ in object_pixels]
    cols = [c for _, c in object_pixels]
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    
    height = max_row - min_row + 1
    width = max_col - min_col + 1

    if height % 2 == 1 and width % 2 == 1:
        center_row = min_row + height // 2
        center_col = min_col + width // 2
        return (center_row, center_col)
    else:
        return None
    

def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    objects = find_objects(input_grid)

    # Gray transformations
    if 5 in objects:
      for gray_object in objects[5]:
          center = find_object_center(gray_object)
          if center:
              center_r, center_c = center
              for r, c in gray_object:
                  if r == center_r and c == center_c:
                      output_grid[r, c] = 4  # Center to yellow
                  else:
                      output_grid[r, c] = 2 # Other gray to red
          else: # no center
              for r, c in gray_object:
                  output_grid[r,c] = 2


    # White transformations (always to red)
    if 0 in objects:
      for white_object in objects[0]:
          for r, c in white_object:
                output_grid[r, c] = 2

    return output_grid
```
