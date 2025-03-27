"""
The transformation rule involves a complex reflection and interaction of objects within the grid.
1. Identify Objects: Group contiguous pixels of the same color.
2. Locate Centers: The output grid is created from the object's components re-arranged.
3. Reflect/Transform: 
    - Invert rows and columns of each object, 
    - Resolve interactions between objects (lower value prevails).
4. Assemble Output: Build the output grid with the transformed objects.
"""

import numpy as np

def get_objects(grid):
    """
    Finds and returns a list of objects in the grid.  Each object is a set
    of (row, col) coordinates.
    """
    objects = []
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def dfs(row, col, current_object):
        if (row, col) in visited or row < 0 or row >= rows or col < 0 or col >= cols or grid[row][col] != grid_value:
            return
        visited.add((row, col))
        current_object.add((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited:
                grid_value = grid[row][col]
                current_object = set()
                dfs(row, col, current_object)
                objects.append((grid_value, current_object))
    return objects

def transform(input_grid):
    # Initialize output_grid with the same dimensions and filled with zeros
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Get objects from the input grid
    objects = get_objects(input_grid)
    
    # Process and reflect each object's coordinates
    for value, obj in objects:
      for r,c in obj:
        output_grid[r][c] = value

    objects = get_objects(output_grid)

    output_grid = np.zeros_like(input_grid)

    for value, obj in objects:
      # build a temp grid from object
      min_r = min([r for r, c in obj])
      max_r = max([r for r, c in obj])
      min_c = min([c for r, c in obj])
      max_c = max([c for r, c in obj])

      temp_grid = np.full((max_r - min_r + 1, max_c - min_c + 1), 0)
      for r, c in obj:
        temp_grid[r - min_r][c - min_c] = value
      
      # invert object rows and cols
      inverted_grid = temp_grid[::-1, ::-1]
      
      # add object to ouput
      for r in range(inverted_grid.shape[0]):
          for c in range(inverted_grid.shape[1]):
              new_r = min_r + r
              new_c = min_c + c
              if (output_grid[new_r][new_c] == 0 or output_grid[new_r][new_c] > inverted_grid[r][c]) and inverted_grid[r][c] != 0:
                output_grid[new_r][new_c] = inverted_grid[r][c]

    return output_grid.tolist()