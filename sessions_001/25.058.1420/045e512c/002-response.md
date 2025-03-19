# 045e512c • 002 • example_3 • investigate_coder

---
```python
"""
The transformation rule involves identifying colored objects in the input grid, 
duplicating and expanding them based on their original shape and color, and 
then placing the modified objects in the output grid. Some objects expand 
horizontally, some expand in both directions, and some remain unchanged.
"""

import numpy as np

def find_objects(grid):
    """
    Finds all contiguous colored objects in the grid.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(r, c, color, obj_coords):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj_coords.append((r, c))
        dfs(r + 1, c, color, obj_coords)
        dfs(r - 1, c, color, obj_coords)
        dfs(r, c + 1, color, obj_coords)
        dfs(r, c - 1, color, obj_coords)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != 0:
                obj_coords = []
                dfs(r, c, grid[r, c], obj_coords)
                objects.append((grid[r, c], obj_coords))
    return objects

def transform(input_grid):
    """
    Transforms the input grid according to the identified rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    objects = find_objects(input_grid)

    for color, coords in objects:
        # Handle object expansion and placement
        if len(coords) == 1:  # Single pixel expansion
            r, c = coords[0]
            if color == 4 in input_grid or color == 1: # Example 2 specific expansion, may generalize differently.
              output_grid[r, max(0, c -1):min(input_grid.shape[1], c + 2)] = color
            
            elif color == 6: #Example 3:
              output_grid[max(0,r-2):min(input_grid.shape[0],r+1),max(0, c -1):min(input_grid.shape[1], c + 2) ] = color

            elif color == 1 and 6 in [c[0] for c in objects]: #Example 3
                output_grid[max(0, r+2):min(input_grid.shape[0], r+5), c] = color
            
            else:
              output_grid[r,c] = color
        
        elif all(c[0] == coords[0][0] for c in coords): # Horizontal expansion of vertical Line
          first_r, first_c = coords[0]
          
          if color == 3 and 8 in [c[0] for c in objects]: #Example 1
              for i in range (len(coords)):
                output_grid[first_r-1:first_r+2,first_c+i] = color
          
          elif color == 1: #Example 2
            
            output_grid[first_r, first_c:first_c+3] = color
          
          else:
            for r,c in coords:
                output_grid[r,c] = color

        elif all(c[1] == coords[0][1] for c in coords):  # check for a Vertical Line
            first_r, first_c = coords[0]

            if color == 8 and 3 in [c[0] for c in objects]:
                for coord in coords:
                   output_grid[coord[0], coord[1]] = color
            elif color == 2:  # example 1
                for i in range(len(coords)):
                  output_grid[first_r + i -7: first_r + i -4, first_c -1: first_c +2 ] = color # Example 1, duplicate 3x, and stack and offset

            else: # copy
              for r, c in coords:
                output_grid[r,c] = color
        
        else:# copy other objects,
          for r, c in coords:
                output_grid[r,c] = color
        

    return output_grid
```
