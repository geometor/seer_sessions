"""
Transforms the input grid by identifying connected regions of specific colors and shapes, then selectively deleting and redrawing parts of these regions.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous regions of the same color in the grid.
    Returns a list of objects, where each object is a set of (row, col) coordinates.
    """
    visited = set()
    objects = []

    def dfs(row, col, color, current_object):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_object.add((row, col))
        dfs(row + 1, col, color, current_object)
        dfs(row - 1, col, color, current_object)
        dfs(row, col + 1, color, current_object)
        dfs(row, col - 1, color, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] != 0 and (row, col) not in visited:
                current_object = set()
                dfs(row, col, grid[row, col], current_object)
                objects.append(current_object)
    return objects

def is_connected(object1, object2):
     """
     check if the objects are neighbor
     """
     for r1,c1 in object1:
          for r2,c2 in object2:
               if abs(r1-r2) + abs(c1-c2) == 1:
                    return True
     return False
               

def transform(input_grid):
    """
    Transforms the input grid according to the observed rules.
    """
    output_grid = np.copy(input_grid)
    objects = find_objects(input_grid)

    for obj1 in objects:
        for obj2 in objects:
            if obj1 != obj2 and is_connected(obj1,obj2):
                 color1 = input_grid[list(obj1)[0][0], list(obj1)[0][1]]
                 color2 = input_grid[list(obj2)[0][0], list(obj2)[0][1]]

                 # case 1
                 if {color1,color2} == {4,5}:
                      if color2 == 5: # obj2 is gray
                           for r,c in obj2: # remove obj2
                                output_grid[r,c] = 0
                      else: # obj1 is gray
                           for r,c in obj1:
                                output_grid[r,c] = 0 
                 # case 2
                 elif {color1,color2} == {2,4}:
                      if color2 == 4:  # obj2 is yellow
                           for r,c in obj2:
                                output_grid[r,c] = 0
                      else:          #obj1 is yellow
                           for r,c in obj1:
                                output_grid[r,c] = 0
                 # case 3
                 elif {color1, color2} == {2,3}:
                      if color2 == 2:          # obj2 is red
                           for r, c in obj2:
                                output_grid[r,c] = 0

                      else:                  # obj1 is red:
                           for r,c in obj1:
                                output_grid[r,c] = 0

    return output_grid