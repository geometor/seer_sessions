# 681b3aeb • 011 • refine_coder

---
```python
"""
1. Create a 3x3 magenta block. This is the top-left of the output.
2. Find yellow objects: Locate the yellow object in the input.
3. Yellow Column: Create a yellow column with height equal to the rows the yellow object would take if stacked vertically.
4. Combine: Stack the yellow column created to the left of the magenta block created before. If a yellow object does not exist, create a black (0) column with the same height as the magenta object.
5. Output Dimensions: The output grid's dimensions are determined by placing the 3x3 magenta block and yellow (or 0) column adjacent to one another.
"""

import numpy as np

def find_objects(grid, color):
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return []
    
    coords = list(zip(rows, cols))
    objects = []

    while coords:
        obj_coords = []
        first_coord = coords.pop(0)
        obj_coords.append(first_coord)

        current_r, current_c = first_coord
        
        to_check = [(current_r, current_c)]
        
        while to_check:
            r, c = to_check.pop(0)
            
            neighbors = [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]

            for nr, nc in neighbors:
                if (nr, nc) in coords:
                    obj_coords.append((nr, nc))
                    coords.remove((nr, nc))
                    to_check.append((nr,nc))


        objects.append(obj_coords)


    return objects
def transform(input_grid):
    # 1. Create a 3x3 magenta block.
    output_grid = np.zeros((3, 3), dtype=int)
    output_grid[:] = 6  # Magenta

    # 2. Find yellow objects.
    yellow_objects = find_objects(input_grid, 4)

    # 3. Yellow Column & 4. Combine
    if yellow_objects:
        # Determine the rows that yellow object occupies
        rows = set()
        for r,c in yellow_objects[0]:
            rows.add(r)
        height = len(rows)
        
        new_output_grid = np.zeros((max(3,height), 4), dtype=int)
        new_output_grid[:height,0] = 4 #yellow column
        new_output_grid[:3, 1:4] = output_grid # magenta block
        output_grid = new_output_grid
    else:
      #If not yellow objects, keep the 3x3 output grid.
      pass
    

    return output_grid
```
