"""
The transformation rule involves identifying non-blue (non-1) colored regions in the input grid and mirroring them vertically.  The mirroring appears to happen relative to a 'red' (2) region when present or other wise use the vertical center of the objects. The order and adjacency of objects is perserved during mirroring.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects in the grid.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, current_object):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, color, current_object)
        dfs(row - 1, col, color, current_object)
        dfs(row, col + 1, color, current_object)
        dfs(row, col - 1, color, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 1:
                current_object = []
                dfs(row, col, grid[row, col], current_object)
                objects.append((grid[row, col], current_object))  # Store color and object
    return objects

def find_lowest_red_block(grid):
    """Finds the lowest 2x2 red block's top-left coordinates."""
    for r in range(grid.shape[0] - 1, -1, -1):
        for c in range(grid.shape[1] - 1):
            if (grid[r, c] == 2 and grid[r + 1, c] == 2 and
                grid[r, c + 1] == 2 and grid[r + 1, c + 1] == 2):
                return r, c
    return None

def transform(input_grid):
    """
    Transforms the input grid according to the mirroring rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    output_grid[:] = 1  # Initialize with blue (1)

    objects = find_objects(input_grid)
    red_block_coords = find_lowest_red_block(input_grid)

    
    if red_block_coords is not None:
      red_row, _ = red_block_coords
      
      for color, obj in objects:
        min_row = min(r for r, _ in obj)
        max_row = max(r for r, _ in obj)
        
        if(max_row > red_row):
          for r, c in obj:
            #mirror objects that are below the red block
            dist_to_red = r - red_row
            
            new_row = red_row - dist_to_red
            
            if(new_row >= 0):
                output_grid[new_row,c] = color
            else:
              output_grid[r,c] = color #default - not mirrored
        else:
          #copy all objects that are above the red block
          for r, c in obj:
            output_grid[r,c] = color #default - not mirrored
    else:
        #no red block - mirror objects across object center line
        object_rows = []

        for color, obj in objects:
            for r, c in obj:
              object_rows.append(r)
            
        if len(object_rows) > 0:

            min_obj_row = min(object_rows)
            max_obj_row = max(object_rows)
            obj_center = (min_obj_row + max_obj_row) / 2

            
            for color, obj in objects:
                for r, c in obj:
                    dist = r - obj_center
                    new_r = int(round(obj_center - dist))
                    if 0 <= new_r < output_grid.shape[0]:
                      output_grid[new_r,c] = color
                    else:
                      output_grid[r,c] = color #default - not mirrored

        else:
            #no objects found.  just return grid
            output_grid = np.copy(input_grid)

    return output_grid.tolist()