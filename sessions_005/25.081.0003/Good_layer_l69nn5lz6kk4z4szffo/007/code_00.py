"""
1.  **Identify Objects:** Divide the input grid into distinct objects. An object is defined as a contiguous region of pixels of the same color.
2.  **Identify Primary and Secondary Objects:** Determine the two primary objects involved in the transformation. The objects form rectangular shapes. Primary objects are those above other objects (when applicable).
3. **Identify the interface**: determine the row of pixels where object_1 is above and adjacent to object_2.
4.  **Shift Boundary:** Shift the boundary between the primary and secondary objects. The shift occurs along their shared horizontal boundary. Specifically, the bottom-most row of the primary object (object_1) that is directly above the secondary object (object_2) moves one unit down, replacing the top-most row of the secondary object directly below.
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

def find_adjacent_objects(objects):
   # identify the two main rectangular blocks that are moving
   # For simplicity, assume the two largest objects by coordinate count are the ones of interest.
   # return them in consistent order (object with smaller color first for consistency, object_1)
    sorted_objects = sorted(objects.values(), key=lambda x: len(x['coords']), reverse=True)
    if len(sorted_objects) < 2:
      return None, None
    
    obj1 = sorted_objects[0]
    obj2 = sorted_objects[1]
    if obj1['color'] > obj2['color']:
        obj1, obj2 = obj2, obj1
        
    return obj1, obj2

def find_interface(obj1, obj2):
    # Find the row where obj1 is directly above obj2
    obj1_coords = set(obj1['coords'])
    obj2_coords = set(obj2['coords'])
    interface_cols = []
    obj1_max_row = -1

    for r1, c1 in obj1_coords:
        if (r1 + 1, c1) in obj2_coords:
            interface_cols.append(c1)
            obj1_max_row = max(obj1_max_row,r1)

    return obj1_max_row, interface_cols


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    grid = np.array(input_grid)

    # Find objects
    objects = find_objects(grid)
   
    # find the two objects
    obj1, obj2 = find_adjacent_objects(objects)
    if obj1 is None or obj2 is None:
       return output_grid

    # Determine transformation: boundary shift.
    # obj1 expands down, obj2 contracts
    # find the interface row of obj1 and obj2 using find_interface

    obj1_max_row, interface_cols = find_interface(obj1,obj2)

    # move the correct pixels
    for col in interface_cols:
        output_grid[obj1_max_row + 1, col] = obj1['color']
    
    return output_grid.tolist()