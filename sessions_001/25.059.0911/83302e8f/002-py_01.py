"""
The transformation identifies a primary shape formed by non-background colored pixels in the input grid.
It then inverts the colors in areas where shape lines intersect and fills parts based on those areas. The colors are changed to predefined colors,
maintaining the overall structure of the original shape but altering its internal color composition.
"""

import numpy as np

def get_objects(grid):
    # Find connected components (objects) in the grid, excluding the background (color 0).

    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, color, obj):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj.append((r, c))
        dfs(r + 1, c, color, obj)
        dfs(r - 1, c, color, obj)
        dfs(r, c + 1, color, obj)
        dfs(r, c - 1, color, obj)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c] and grid[r, c] != 0:
                obj = []
                dfs(r, c, grid[r, c], obj)
                objects.append(obj)
    return objects

def transform(input_grid):
    # Initialize output grid with a copy of the input grid
    output_grid = np.copy(input_grid)

    # Get objects in input
    objects = get_objects(input_grid)

    # identify color of objects
    color_map_output = {
      8 : [8,4,3],
      1 : [1,4,3],
      9 : [9,4,3]
    }

    # Iterate each objects
    for obj in objects:
      first_pixel = obj[0]
      color = input_grid[first_pixel]
      # print("obj color=",color)

      # build matrix of the obj
      rows, cols = zip(*obj)
      min_row, max_row = min(rows), max(rows)
      min_col, max_col = min(cols), max(cols)

      obj_grid = np.zeros((max_row - min_row + 1, max_col - min_col + 1), dtype=int)

      for r,c in obj:
        obj_grid[r-min_row,c-min_col] = input_grid[r,c]


      for r, c in obj:
        # detect crossing
        if (r > 0 and r+1 < input_grid.shape[0] and
            c > 0 and c+1 < input_grid.shape[1] and
            input_grid[r - 1, c] == color and
            input_grid[r + 1, c] == color and
            input_grid[r , c-1] == color and
            input_grid[r , c+1] == color
            ):
              # invert crossing
              # print("inverting",r,c)
              output_grid[r,c] = color_map_output[color][1]
        elif (r > 0 and r < input_grid.shape[0] -1 and
            input_grid[r-1,c] == color and input_grid[r+1,c] == color):
              if ( (c > 0 and input_grid[r,c-1] != color) or c==0) and ( (c < input_grid.shape[1] -1 and input_grid[r,c+1] != color) or c == input_grid.shape[1] -1):
                output_grid[r,c] = color_map_output[color][0]
              else:
                output_grid[r,c] = color_map_output[color][2]
        elif (c > 0 and c < input_grid.shape[1] -1 and
            input_grid[r,c-1] == color and input_grid[r,c+1] == color):
              if ( (r > 0 and input_grid[r-1,c] != color) or r==0) and (( r < input_grid.shape[0] -1 and input_grid[r+1,c] != color) or r == input_grid.shape[0]-1):
                output_grid[r,c] = color_map_output[color][0]
              else:
                output_grid[r,c] = color_map_output[color][2]
        else:
           output_grid[r,c] = color_map_output[color][0]

    return output_grid