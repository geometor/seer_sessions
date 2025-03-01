"""
1.  **Identify Input Objects:** Scan the input grid and identify all contiguous regions of red (2) pixels. Each contiguous region is considered a single object.
2.  **Process Each Object:** For each identified red object:
    *   Locate the "inner" edges of the red object.
    *   Create new object by taking a subset of the red object. It is a rectangular region colored green (3).
    *   Replace only red object from the input object with green.
3.  **Preserve Background:**  All white (0) pixels in the input grid remain unchanged in the output grid.
4. The output are green objects corresponding to portions of original red objects.
"""

import numpy as np

def find_objects(grid, color):
    # Find all objects of a specific color in the grid.
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, current_object):
        # Depth-first search to find connected components.
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def get_bounding_box(obj):
    # Get bounding box of object
    min_row = min(obj, key=lambda item: item[0])[0]
    max_row = max(obj, key=lambda item: item[0])[0]
    min_col = min(obj, key=lambda item: item[1])[1]
    max_col = max(obj, key=lambda item: item[1])[1]

    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    # find red objects
    red_objects = find_objects(input_grid, 2)

    # change output pixels
    for obj in red_objects:
      min_row, max_row, min_col, max_col = get_bounding_box(obj)

      if (max_row - min_row +1) * (max_col - min_col+1)  > 4:
        for r, c in obj:
          output_grid[r,c] = 0
        
        if max_row - min_row > 1:
            output_grid[min_row+1, min_col+1:max_col] = 3

        if max_row - min_row > 3:
            output_grid[min_row+2, min_col+1:max_col] = 3
        
        if max_row - min_row > 5:
            output_grid[min_row+3, min_col+1:max_col] = 3
      elif len(obj)>0:
          output_grid[obj[0][0],obj[0][1]] = 3
          if len(obj) > 2:
            output_grid[obj[1][0],obj[1][1]] = 3
            
    return output_grid