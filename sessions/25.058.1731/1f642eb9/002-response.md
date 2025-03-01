# 1f642eb9 • 002 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Objects:** Locate all contiguous blocks of the same color within the input grid. Consider single pixels as individual objects.
2.  **Preserve Background**: Copy all background color from input to ouput.
3.  **Copy the azure object:** Copy the azure colored pixels from input to same location.
4.  **Process Single-Pixel Objects:** For each single-pixel object, copy its color value c, from input grid to output grid.
    *    If c is present in the top row of the input, replace color of pixel directly above the top-most and leftmost azure object pixel with c.
    *    If c is at a location other than the top row, copy it at position left of the top-most and left-most azure pixel of its respective row.
5. If an input color c exists at multiple non-top row locations, create additional copies adjacent to the top-most and left-most pixel of the azure object.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects and single-pixel objects in the grid."""
    objects = {}
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, color, obj_coords):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj_coords.append((r, c))
        dfs(r + 1, c, color, obj_coords)
        dfs(r - 1, c, color, obj_coords)
        dfs(r, c + 1, color, obj_coords)
        dfs(r, c - 1, color, obj_coords)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c] and grid[r,c] != 0:
                color = grid[r, c]
                obj_coords = []
                dfs(r, c, color, obj_coords)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj_coords)

    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # find all objects
    objects = find_objects(input_grid)
    
    #Preserve background
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if input_grid[r,c] == 0:
                output_grid[r,c] = 0
    
    #Copy azure object
    if 8 in objects:
      for azure_obj in objects[8]:
          for r,c in azure_obj:
              output_grid[r,c] = 8

    #Process single pixel objects
    for color, object_list in objects.items():
      if color != 8:
        for obj in object_list:
          if len(obj) == 1:  # Single-pixel object
            r,c = obj[0]
            
            # Copy single pixel object color
            output_grid[r,c] = color
                
            # find top-left azure pixel
            if 8 in objects:
              min_r = input_grid.shape[0]
              min_c = input_grid.shape[1]

              for azure_obj in objects[8]:
                for ar, ac in azure_obj:
                  if ar<min_r:
                    min_r = ar
                    min_c = ac
                  elif ar==min_r and ac < min_c:
                    min_c = ac

              # If present in top row, replace color above azure
              if r == 0:
                  if min_r > 0:
                      output_grid[min_r -1, min_c] = color
              # else copy left of azure
              else:
                  output_grid[min_r, min_c -1] = color
    return output_grid
```
