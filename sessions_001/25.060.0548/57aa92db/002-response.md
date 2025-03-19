# 57aa92db • 002 • example_4 • investigate_coder

---
```python
"""
Extends background colored objects adjacent to other objects, effectively combining them.
"""

import numpy as np

def get_objects(grid):
    """
    Identifies and returns a list of objects in the grid.
    Each object is a set of (row, col) coordinates.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color, obj):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
            return
        visited.add((r, c))
        obj.add((r, c))
        dfs(r + 1, c, color, obj)
        dfs(r - 1, c, color, obj)
        dfs(r, c + 1, color, obj)
        dfs(r, c - 1, color, obj)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                obj = set()
                dfs(r, c, grid[r, c], obj)
                objects.append((grid[r,c], obj))  # Store color along with object coordinates
    return objects

def is_background(obj_data, grid_shape):
    """Determines if the given object represents background
    """
    color, obj = obj_data
    rows, cols = grid_shape

    # Check if the object touches all edges of the grid
    top_edge = any(r == 0 for r, _ in obj)
    bottom_edge = any(r == rows - 1 for r, _ in obj)
    left_edge = any(c == 0 for _, c in obj)
    right_edge = any(c == cols - 1 for _, c in obj)
    
    return top_edge and bottom_edge and left_edge and right_edge

def transform(input_grid):
    """
    Extends background colored objects that are adjacent to other objects.
    """
    grid = np.array(input_grid)  # Convert to NumPy array
    rows, cols = grid.shape
    output_grid = grid.copy()

    objects = get_objects(grid)

    # Determine background objects.
    background_objects = []
    for obj_data in objects:
      if is_background(obj_data, grid.shape):
        background_objects.append(obj_data)
    
    #print(background_objects)
        
    # Extend background object pixels
    for background_color, background_obj in background_objects:
       #print(f"bg color {background_color}")
       new_background = set()
       for r,c in background_obj:
           new_background.add((r,c)) # add existing bg

       # expand the current object, 1 iteration at a time
       extended = True
       while extended:
        extended = False
        to_add = set()
        for r, c in new_background:
           neighbors = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
           for nr, nc in neighbors:
            if 0 <= nr < rows and 0 <= nc < cols: # bounds check
               if (nr,nc) not in new_background: # only grow to places not already the same color
                to_add.add((nr, nc)) # all neighbors added
                extended = True # loop while we keep expanding


        # after 1 pass, add to_add
        #print(to_add)
        for r,c in to_add:
           output_grid[r,c] = background_color # set bg
           new_background.add((r,c)) # now add to growing bg set

    return output_grid.tolist()
```
