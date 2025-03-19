# bc1d5164 • 020 • refine_coder

---
```python
"""
1. Identify Objects: Divide the input grid into distinct objects based on contiguous regions of the same color.
2. Identify Background: White (color 0) objects are considered "background".
3. Remove Background: Discard all background objects.
4. Preserve Other Objects: All other objects and their positions and size remain unchanged.
5. Output: The output grid retains the size and shape of the original *largest* object, which is the azure object in all of these examples. Any space not occupied by the remaining objects are filled based on the background of that area in the input.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects in a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(row, col, color, object_coords):
        if (row < 0 or row >= rows or col < 0 or col >= cols or
            visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        object_coords.append((row, col))
        dfs(row + 1, col, color, object_coords)
        dfs(row - 1, col, color, object_coords)
        dfs(row, col + 1, color, object_coords)
        dfs(row, col - 1, color, object_coords)

    for row in range(rows):
        for col in range(cols):
            if not visited[row, col]:
                color = grid[row, col]
                object_coords = []
                dfs(row, col, color, object_coords)
                if object_coords:
                    objects.append({'color': color, 'coords': object_coords})
    return objects

def get_largest_object(objects):
    """ returns the object with the most pixels """
    largest_object = None
    max_size = 0
    
    for obj in objects:
      obj_size = len(obj['coords'])
      if obj_size > max_size:
        max_size = obj_size
        largest_object = obj
        
    return largest_object
    

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify Objects
    objects = find_objects(input_grid)

    # 2. & 3. Identify and Remove Background (White objects)
    non_background_objects = [obj for obj in objects if obj['color'] != 0]
    
    # find largest object
    largest_object = get_largest_object(objects)

    # 4. Preserve Other Objects & 5. Output Grid
    output_grid = np.full((len(largest_object['coords']) // max(rows, cols), max(rows, cols)), largest_object['color'])

    for obj in non_background_objects:
        for row, col in obj['coords']:
            # make sure we don't try to write outside of output array
            if row < output_grid.shape[0] and col < output_grid.shape[1]:
                output_grid[row, col] = obj['color']

    return output_grid.tolist()
```
