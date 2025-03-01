# 5117e062 • 002 • example_3 • investigate_coder

---
```python
"""
The transformation rule involves identifying distinct colored objects in the input grid, selecting one based on some criteria, and reproducing its shape and color in a 3x3 output grid with a white background. The selection criteria is to find a non-white object with pixels in the shape of a plus sign.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects in a grid.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_pixels):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                obj_pixels = []
                dfs(row, col, grid[row, col], obj_pixels)
                objects.append({'color': grid[row, col], 'pixels': obj_pixels})
    return objects

def is_plus_shape(pixels, color, grid):
    """
    Checks if the given pixels form a plus shape.
    """
    if len(pixels) != 5:
        return False

    # Convert pixel coordinates to a set for efficient lookup
    pixel_set = set(pixels)

    # Find the center pixel (the one with 4 neighbors of the same color)
    center_pixel = None
    for r, c in pixels:
        neighbors = 0
        if (r + 1, c) in pixel_set:
            neighbors += 1
        if (r - 1, c) in pixel_set:
            neighbors += 1
        if (r, c + 1) in pixel_set:
            neighbors += 1
        if (r, c - 1) in pixel_set:
            neighbors += 1
        if neighbors == 4:
            center_pixel = (r, c)
            break
    
    if center_pixel is None: return False
    
    r, c = center_pixel
    
    # Check that it has neighbors on all four sides
    if (r+1, c) not in pixel_set:
        return False
    if (r-1, c) not in pixel_set:
        return False    
    if (r, c+1) not in pixel_set:
        return False    
    if (r, c-1) not in pixel_set:
        return False        
            
    return True

def transform(input_grid):
    """
    Transforms the input grid according to the identified rule.
    """
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Find objects
    objects = find_objects(input_grid)
    
    selected_object = None
    # Select the plus-shaped object
    for obj in objects:
      if is_plus_shape(obj['pixels'], obj['color'], input_grid):
        selected_object = obj
        break
        
    if selected_object is None:
      for obj in objects:
        if len(obj['pixels']) == 5:
            selected_object = obj
            break
        
    if selected_object is None:
      return output_grid

    # Extract color of selected object.
    color = selected_object['color']

    # Create plus shape in the center of the output grid
    output_grid[1, 1] = color
    output_grid[0, 1] = color
    output_grid[2, 1] = color
    output_grid[1, 0] = color
    output_grid[1, 2] = color
    

    return output_grid
```
