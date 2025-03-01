# e76a88a6 • 002 • example_2 • investigate_coder

---
```python
"""
The transformation identifies the grey (color 5) colored object and changes it to the color(s) of the object in the upper-left.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous regions of the same color (excluding 0) in a grid.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, color, obj_coords):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj_coords.append((r, c))
        dfs(r + 1, c, color, obj_coords)
        dfs(r - 1, c, color, obj_coords)
        dfs(r, c + 1, color, obj_coords)
        dfs(r, c - 1, color, obj_coords)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c] and grid[r, c] != 0:
                obj_coords = []
                dfs(r, c, grid[r, c], obj_coords)
                objects.append({'color': grid[r, c], 'coords': obj_coords})
    return objects

def get_top_left_object(objects):
    """
    Gets the object whose bounding box's top-left corner is most top-left.
    """
    if not objects:
        return None
    
    #Find min row and then min col for that row
    min_row = min(min(coord[0] for coord in obj['coords']) for obj in objects)
    min_col_at_min_row = min(min(coord[1] for coord in obj['coords'] if min(cr[0] for cr in obj['coords']) == min_row )  for obj in objects )

    for obj in objects:
      if min(coord[0] for coord in obj['coords']) == min_row:
        if min(coord[1] for coord in obj['coords']) == min_col_at_min_row:
          return obj
    
    return None #should never occur
    

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)

    # Find all objects
    objects = find_objects(input_grid)

    #find top left object
    top_left_object = get_top_left_object(objects)

    # Find the gray (color 5) object
    gray_object = next((obj for obj in objects if obj['color'] == 5), None)
    
    if gray_object and top_left_object:
        # recolor the gray object
        replacement_colors = np.zeros_like(input_grid)
        for r,c in top_left_object['coords']:
            replacement_colors[r,c] = input_grid[r,c]

        #recolor based on topleft object, offset by position of grey object
        top_left_row_offset = min( coord[0] for coord in gray_object['coords'] ) - min( coord[0] for coord in top_left_object['coords'] )
        top_left_col_offset = min( coord[1] for coord in gray_object['coords'] ) - min( coord[1] for coord in top_left_object['coords'] )
        for r, c in gray_object['coords']:
            replacement_r = r - top_left_row_offset
            replacement_c = c - top_left_col_offset
            if 0 <= replacement_r < input_grid.shape[0] and 0 <= replacement_c < input_grid.shape[1]:
                output_grid[r, c] = replacement_colors[replacement_r,replacement_c]

    return output_grid.tolist()
```
