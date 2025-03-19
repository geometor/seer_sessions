# b775ac94 • 010 • example_2 • investigate_coder

---
```python
"""
The transformation rule involves identifying colored objects in the input grid, 
creating a vertically mirrored copy of these objects, scaling both object sets by a factor of x2 and placing the mirrored set below the original.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies distinct objects in the grid.
    Returns a dictionary of objects, where each object is represented by a list of its pixel coordinates.
    """
    objects = {}
    visited = set()

    def get_neighbors(r, c):
        neighbors = []
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1]:
                neighbors.append((nr, nc))
        return neighbors

    def dfs(r, c, color, obj_id):
        visited.add((r, c))
        objects[obj_id].append((r, c))

        for nr, nc in get_neighbors(r, c):
            if (nr, nc) not in visited and grid[nr, nc] == color:
                dfs(nr, nc, color, obj_id)

    obj_id_counter = 0
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0 and (r, c) not in visited:
                objects[obj_id_counter] = []
                dfs(r, c, grid[r, c], obj_id_counter)
                obj_id_counter += 1
    return objects

def reflect_and_scale_objects(objects, grid):
    """Reflect, scale, and translate objects."""

    scaled_objects = {}

    max_row = 0
    for obj_id, pixels in objects.items():
       for r,c in pixels:
          if r > max_row:
             max_row = r
    row_offset = max_row + 1

    
    for obj_id, pixels in objects.items():
       scaled_objects[obj_id] = []
       scaled_objects[obj_id + len(objects)] = [] # + len to create a separate id for reflected and scaled objects

       for r, c in pixels:

          # scale and translate original object          
          scaled_objects[obj_id].append( (2*r - 2*(row_offset - 1) , 2*c) )
          scaled_objects[obj_id].append( (2*r - 2*(row_offset - 1) , 2*c + 1) )
          scaled_objects[obj_id].append( (2*r + 1 - 2*(row_offset - 1) , 2*c) )
          scaled_objects[obj_id].append( (2*r + 1 - 2*(row_offset - 1) , 2*c + 1) )

          # scale, reflect and translate
          scaled_objects[obj_id + len(objects)].append( (2*r + 2*row_offset - (2 * (row_offset -1)) , 2*c) )
          scaled_objects[obj_id + len(objects)].append( (2*r + 2*row_offset - (2 * (row_offset - 1)) , 2*c + 1) )          
          scaled_objects[obj_id + len(objects)].append( (2*r + 1 + 2*row_offset - (2* (row_offset -1)), 2*c) )
          scaled_objects[obj_id + len(objects)].append( (2*r + 1 + 2*row_offset - (2* (row_offset -1)), 2*c + 1) )          

    return scaled_objects

def transform(input_grid):
    """
    Transforms the input grid according to the defined rule.
    """
    input_grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation

    # Find all distinct objects in the input grid
    objects = find_objects(input_grid)
        
    # Scale and reflect the objects
    scaled_objects = reflect_and_scale_objects(objects, input_grid)

    # Determine the size of the output grid based on scaled objects
    max_r = 0
    max_c = 0
    for obj_pixels in scaled_objects.values():
      for r,c in obj_pixels:
        max_r = max(r,max_r)
        max_c = max(c,max_c)
    
    output_grid = np.zeros((max_r + 1, max_c + 1), dtype=int)

    # Fill the output grid
    for obj_id, pixels in scaled_objects.items():
        for r, c in pixels:
            # Get original object color. obj_id can be larger than original object set.
            original_obj_id = obj_id % len(objects)
            color = input_grid[objects[original_obj_id][0][0], objects[original_obj_id][0][1]] # get color of first pixel.            
            if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:  # boundary check
                output_grid[r, c] = color
            else:
               print("Warning - out of bounds")

    return output_grid.tolist() # return as list
```
