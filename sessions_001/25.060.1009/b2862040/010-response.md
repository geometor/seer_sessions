# b2862040 • 010 • refine_coder

---
```python
"""
1.  **Identify Objects:** Find all distinct objects within the input grid. An object is a group of connected pixels of the same color that are not the background color.
2.  **Exactly One Change**: Of all of the objects in the input, *exactly one* will change colors.
3. **New Color**: The changed object will transform to a specific color.
4. **Preserve Unchanged**: The other object (or objects) will not have its color changed.
5. **No Shape Changes**: All objects will retain their input shapes in the output.
6. **Output Grid**: return the modified input as the output.
"""

import numpy as np

def find_objects(grid, background_color=9):
    """
    Finds connected regions of pixels with the same color (objects) in the grid.
    """
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col, color, obj_coords):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        obj_coords.append((row, col))
        dfs(row + 1, col, color, obj_coords)
        dfs(row - 1, col, color, obj_coords)
        dfs(row, col + 1, color, obj_coords)
        dfs(row, col - 1, color, obj_coords)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != background_color:
                color = grid[row, col]
                obj_coords = []
                dfs(row, col, color, obj_coords)
                objects.append({"color": color, "coords": obj_coords})
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # find the objects
    objects = find_objects(input_grid)

    # Determine which object changes and to what color based on the examples.
    # we will pick the *first* object
    if len(objects) > 0:
       changed_object = objects[0]
       original_color = changed_object['color']
       
       #get new color from the examples (and check for errors)
       new_color = None
       for row in range(input_grid.shape[0]):
           for col in range(input_grid.shape[1]):
               if input_grid[row,col] != output_grid[row,col]:
                   if new_color is None:
                       new_color = output_grid[row,col]
                   elif new_color != output_grid[row,col]:
                       raise Exception("multiple color changes detected")

       if new_color is not None:  # if a color change is even present in example
         for row, col in changed_object['coords']:
            output_grid[row,col] = new_color

    return output_grid
```

