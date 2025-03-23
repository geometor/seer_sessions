```python
"""
Identify two primary adjacent objects. Shift the boundary between them such that one object
expands downwards or rightwards by one unit along the boundary, and the other object correspondingly shrinks.
"""

import numpy as np

def find_objects(grid):
    # Find distinct objects (contiguous blocks of same color)
    objects = {}
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_id):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        objects[obj_id]['coords'].append((row, col))
        dfs(row + 1, col, color, obj_id)
        dfs(row - 1, col, color, obj_id)
        dfs(row, col + 1, color, obj_id)
        dfs(row, col - 1, color, obj_id)

    obj_id = 0
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                objects[obj_id] = {'color': grid[row, col], 'coords': []}
                dfs(row, col, grid[row, col], obj_id)
                obj_id += 1

    return objects

def find_moving_objects(objects, grid):
    # Find the two objects that are involved in the boundary shift
    # Prioritize non-background colors for movement
    
    moving_objects = []
    for obj_id, obj_data in objects.items():
      if obj_data['color'] != 0:
        moving_objects.append(obj_data)
    
    # if we only have one object, and background, no moves
    if len(moving_objects) < 2:
      return None, None

    # Find the object pair with the longest shared boundary.
    max_shared_boundary = -1
    obj1 = None
    obj2 = None
    
    for i in range(len(moving_objects)):
        for j in range(i + 1, len(moving_objects)):
            shared_boundary = 0
            for r1, c1 in moving_objects[i]['coords']:
                for r2, c2 in moving_objects[j]['coords']:
                    if abs(r1 - r2) + abs(c1 - c2) == 1:
                        shared_boundary += 1

            if shared_boundary > max_shared_boundary:
                max_shared_boundary = shared_boundary
                obj1 = moving_objects[i]
                obj2 = moving_objects[j]
    if obj1['color'] > obj2['color']:
      obj1,obj2 = obj2,obj1

    return obj1, obj2
  

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    grid = np.array(input_grid)

    # Find objects
    objects = find_objects(grid)
   
    # find the two objects
    obj1, obj2 = find_moving_objects(objects, grid)
    if obj1 is None or obj2 is None:
       return output_grid

    # Determine transformation: boundary shift.
    # obj1 expands down or right, obj2 contracts up or left
    
    obj1_coords = obj1['coords']
    obj2_coords = obj2['coords']

    # find boundary and move
    for r1, c1 in obj1_coords:
        for r2, c2 in obj2_coords:
            if abs(r1 - r2) + abs(c1 - c2) == 1:  # Adjacent
                if r1 < r2 : # obj1 above obj2, move down
                  output_grid[r2,c2] = obj1['color']
                elif r1 > r2: # obj2 above obj 1, move up into obj1
                  output_grid[r1,c1] = obj2['color']
                elif c1 < c2: # obj1 is left, move right
                  output_grid[r2,c2] = obj1['color']
                elif c1 > c2: #obj2 is left, move left
                  output_grid[r1, c1] = obj2['color']

    
    return output_grid.tolist()
```