"""
The transformation identifies distinct colored objects in the input grid, determines a bounding box encompassing these objects, and crops the input grid to this bounding box, rearranging the objects within a new, smaller grid.
"""

import numpy as np

def get_objects(grid):
    """
    Identifies and returns a list of distinct colored objects in the grid.
    Each object is represented as a list of (row, col) coordinates.
    """
    objects = {}
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, color, obj):
        if (row, col) in visited or row < 0 or row >= rows or col < 0 or col >= cols or grid[row, col] != color:
            return
        visited.add((row, col))
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for row in range(rows):
        for col in range(cols):
            color = grid[row, col]
            if color != 0 and (row, col) not in visited:
                obj = []
                dfs(row, col, color, obj)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj)
    return objects
                

def bounding_box(objects):
    """
    Calculates the smallest rectangular bounding box encompassing all objects.
    Returns (min_row, min_col, max_row, max_col).
    """
    min_row, min_col = float('inf'), float('inf')
    max_row, max_col = float('-inf'), float('-inf')

    for color, object_groups in objects.items():
        for obj in object_groups:
            for row, col in obj:
                min_row = min(min_row, row)
                min_col = min(min_col, col)
                max_row = max(max_row, row)
                max_col = max(max_col, col)
    return min_row, min_col, max_row, max_col

def get_object_bounding_box(obj):
    """Calculates the bounding box for a single object."""
    min_row, min_col = float('inf'), float('inf')
    max_row, max_col = float('-inf'), float('-inf')
    for row, col in obj:
        min_row = min(min_row, row)
        min_col = min(min_col, col)
        max_row = max(max_row, row)
        max_col = max(max_col, col)
    return min_row, min_col, max_row, max_col


def transform(input_grid):
    # Identify distinct colored objects
    objects = get_objects(input_grid)

    # Determine the bounding box encompassing all objects
    min_row, min_col, max_row, max_col = bounding_box(objects)
    
    # Determine dimension of new array
    rows, cols = max_row - min_row + 1, max_col-min_col+1
    output_grid = np.zeros((rows, cols), dtype=int)
    
    # sort by top left corner
    sorted_objects = []
    for color, obj_list in objects.items():
        for obj in obj_list:
           ob_min_row, ob_min_col, ob_max_row, ob_max_col = get_object_bounding_box(obj)
           sorted_objects.append((color, obj, (ob_min_row, ob_min_col, ob_max_row, ob_max_col) ))

    sorted_objects.sort(key=lambda x: (x[3][0], x[3][1])) # sort by topleft corner of each object's bounding box

    
    # blit object to output grid
    # translate to new origin
    # keep track of grid size
    
    
    output_grid_rows = 0
    output_grid_cols = 0
    
    for color, obj, obj_bb in sorted_objects:
      # get object bounding box
      ob_min_row, ob_min_col, ob_max_row, ob_max_col = obj_bb
      
      # blit object to grid
      o_rows = ob_max_row - ob_min_row + 1
      o_cols = ob_max_col - ob_min_col + 1

      for r in range(o_rows):
          for c in range(o_cols):
              output_grid[r,c] = input_grid[ob_min_row+r, ob_min_col+c]

    return output_grid