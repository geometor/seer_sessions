"""
Identify a hollow square of yellow pixels and a solid square of red pixels in the input grid. Extract the 2x2 subgrid of yellow pixels positioned at the top-left corner of the larger yellow square. Output this 2x2 subgrid.
"""

import numpy as np

def get_objects(grid):
    """
    Find contiguous regions of the same color and return them as a list of objects.
    Each object is a dictionary containing the color, and the set of (row, col) coordinates.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, color, obj_coords):
        if (row, col) in visited or row < 0 or row >= rows or col < 0 or col >= cols or grid[row, col] != color:
            return
        visited.add((row, col))
        obj_coords.add((row, col))
        dfs(row + 1, col, color, obj_coords)
        dfs(row - 1, col, color, obj_coords)
        dfs(row, col + 1, color, obj_coords)
        dfs(row, col - 1, color, obj_coords)

    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited:
                color = grid[row, col]
                if color != 0:
                  obj_coords = set()
                  dfs(row, col, color, obj_coords)
                  objects.append({"color": color, "coords": obj_coords})
    return objects

def transform(input_grid):
    """
    Extracts the top-left 2x2 subgrid of the yellow object.
    """
    # Find objects
    objects = get_objects(input_grid)

    # Find the yellow object
    yellow_object = None
    for obj in objects:
        if obj['color'] == 4:
            yellow_object = obj
            break
    
    # initialize with background
    output_grid = np.zeros((2,2), dtype=int)

    if yellow_object:

      # Get the top-left corner coordinates of the yellow object
      min_row = min(coord[0] for coord in yellow_object['coords'])
      min_col = min(coord[1] for coord in yellow_object['coords'])
      
      # copy the 2x2 region
      for r in range(2):
        for c in range(2):
            output_grid[r,c] = input_grid[min_row+r,min_col+c]

    return output_grid