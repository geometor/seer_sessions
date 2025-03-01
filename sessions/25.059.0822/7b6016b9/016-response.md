# 7b6016b9 • 016 • example_3 • investigate_coder

---
```python
"""
1. Fill the background: Change all pixels with the value 0 (white) in the input to 3 (green) in the output.
2. Preserve Outer Shape: Keep most of the yellow (4) pixels that form the outer "W" shape.
3. Fill Interior: Change all the green (3) pixels, that are *inside* the "W" to 2 (red). Inside is up, down, left, right, no diagonals.
"""

import numpy as np

def get_objects(grid, color):
    """
    Finds objects of a specific color in the grid.
    An "object" is a set of orthogonally connected pixels of the same color.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, current_object):
      
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return

        visited[r, c] = True
        current_object.append((r, c))

        # Explore orthogonal neighbors (up, down, left, right)
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and not visited[r, c]:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def is_inside_w(r, c, w_objects, grid_shape):
    """
    Checks if a given cell (r, c) is "inside" the "W" shape, 
    considering only orthogonal (up, down, left, right) boundaries.
    
    The logic assumes that we're looking for locations within the
    concave sections of the W.
    """

    # Find the W object that the (r,c) might reside within
    
    for w_object in w_objects:
      if (r,c) in w_object:
        return False

    # Ray casting to determine inside/outside
    w_pixels = set()
    for obj in w_objects:
        w_pixels.update(obj)

    # count intersections in all four directions.
    
    up_count = 0
    for i in range(0,r):
      if (i,c) in w_pixels:
        up_count+=1
        
    down_count = 0
    for i in range(r+1,grid_shape[0]):
      if (i,c) in w_pixels:
        down_count+=1

    left_count = 0
    for i in range(0,c):
      if (r,i) in w_pixels:
        left_count+=1
    
    right_count = 0
    for i in range(c+1, grid_shape[1]):
      if (r,i) in w_pixels:
        right_count+=1

    if up_count > 0 and down_count > 0 and left_count > 0 and right_count > 0:
        return True

    return False
    

def transform(input_grid):
    # Initialize output_grid with green (3) - filling the background
    output_grid = np.full_like(input_grid, 3)

    # Preserve Outer Shape: Copy yellow (4) pixels from input to output
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if input_grid[r, c] == 4:
                output_grid[r, c] = 4
                
    w_objects = get_objects(output_grid, 4)

    # Fill Interior: Change green (3) pixels inside the "W" to red (2)
    for r in range(output_grid.shape[0]):
        for c in range(output_grid.shape[1]):
            if output_grid[r, c] == 3:
                if is_inside_w(r, c, w_objects, output_grid.shape):
                    output_grid[r, c] = 2

    return output_grid
```
