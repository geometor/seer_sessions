# d5d6de2d • 004 • example_1 • investigate_coder

---
```python
"""
1. Identify Red Shapes: Locate all contiguous regions of '2' (red) pixels in the input grid.
2. Color Transformation: Change the identified pixel's value '2' to '3', thus switching color red into green.
3. Shape Abstraction:
    *   For the top-most red shape, replace it with a single '3' (green) pixel at any coordinate within the original shape bound.
    *   For the bottom-most red shape, replace it with a 2x2 block of '3' (green) pixels. The position of the top-left corner of this 2x2 block can be anywhere along the top edge of boundary of original red shape.
4. Background Preservation: All '0' (white) pixels in the input grid remain unchanged.
"""

import numpy as np

def find_objects(grid, color):
    """Finds connected regions of the specified color."""
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col, current_object):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    output_grid[:] = 0

    # find red objects
    red_objects = find_objects(input_grid, 2)
    
    # sort objects based on top-most row (y-coordinate)
    red_objects.sort(key=lambda obj: min(pixel[0] for pixel in obj))

    # change output pixels based on shape abstraction rules
    if len(red_objects) >= 1:
        # Top shape becomes a single point
        top_object = red_objects[0]
        output_grid[top_object[0][0], top_object[0][1]] = 3

    if len(red_objects) >= 2:
      # Bottom shape becomes a 2x2 block
        bottom_object = red_objects[1]
        #Find top row of the object
        top_row = min(pixel[0] for pixel in bottom_object)
        #find the left most pixel in top row
        top_row_pixels = [pixel for pixel in bottom_object if pixel[0] == top_row]
        top_left_pixel = min(top_row_pixels, key=lambda pixel:pixel[1])
        output_grid[top_left_pixel[0], top_left_pixel[1]] = 3
        output_grid[top_left_pixel[0], top_left_pixel[1] + 1] = 3
        output_grid[top_left_pixel[0] + 1, top_left_pixel[1]] = 3
        output_grid[top_left_pixel[0] + 1, top_left_pixel[1] + 1] = 3

    return output_grid
```
