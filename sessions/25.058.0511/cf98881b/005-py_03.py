"""
1.  **Fixed Output Size:** The output grid is always 4x4.
2.  **Default Background:** The output grid is filled with black (color 0) by default.
3.  **Yellow Columns:** If there's a yellow (color 4) object in the input, create two columns in the output grid. The first column is at index 1, the second at index 3.
4.  **Blue Overlay:** If there's a blue (color 1) object in the *top left* of the input, place two blue pixels vertically starting at the top of column 2 in the output grid.
"""

import numpy as np

def get_objects(grid, color):
    # Find all pixels of the specified color
    pixels = np.argwhere(grid == color)
    if pixels.size == 0:
        return []

    objects = []
    visited = set()

    def dfs(r, c, current_object):
        if (r, c) in visited or not (0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r,c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r, c in pixels:
         if (r, c) not in visited:
            current_object = []
            dfs(r,c,current_object)
            objects.append(current_object)
    return objects

def transform(input_grid):
    # initialize output_grid as 4x4 and filled with black (0)
    output_grid = np.zeros((4, 4), dtype=int)

    # Check for yellow objects
    yellow_objects = get_objects(input_grid, 4)
    if yellow_objects:
        # Create yellow columns at index 1 and 3
        output_grid[:, 1] = 4
        output_grid[:, 3] = 4

    #check for blue object in top left
    blue_objects = get_objects(input_grid, 1)
    if blue_objects:
      is_top_left = False
      for r,c in blue_objects[0]:
        if r < 3 and c < 3:
          is_top_left = True
          break
      if is_top_left:
        output_grid[0,2] = 1
        output_grid[1,2] = 1

    return output_grid