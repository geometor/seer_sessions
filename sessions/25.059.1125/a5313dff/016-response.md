# a5313dff • 016 • example_3 • investigate_coder

---
```python
"""
The transformation rule is to identify the contiguous region of red (2) pixels and then fill any enclosed white (0) areas within that red region with blue (1). The red pixels themselves remain unchanged, as do any white pixels not enclosed by red.
"""

import numpy as np
from scipy.ndimage import label

def find_objects(grid, color):
    """Find contiguous regions of the specified color."""
    color_mask = (grid == color)
    labeled_array, num_features = label(color_mask)
    objects = []
    for i in range(1, num_features + 1):
        objects.append(np.where(labeled_array == i))
    return objects

def is_enclosed(obj, red_object, grid_shape):
    """Check if an object (white area) is fully enclosed by the red object."""
    min_row, max_row = grid_shape[0], -1
    min_col, max_col = grid_shape[1], -1
    
    for r, c in zip(obj[0], obj[1]):
        min_row = min(min_row, r)
        max_row = max(max_row, r)
        min_col = min(min_col, c)
        max_col = max(max_col, c)
    
    # Check for boundary conditions. If any part of the obj is touching the edge of the image, then return immediately
    if min_row == 0 or max_row == grid_shape[0]-1 or min_col == 0 or max_col == grid_shape[1] -1:
        return False

    #Check the neighbors (up, down, left, and right) of each cell
    for r, c in zip(obj[0], obj[1]):
        neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        for nr, nc in neighbors:
            if (nr,nc) not in zip(red_object[0], red_object[1]) and (nr,nc) not in zip(obj[0], obj[1]):
               return False
    return True


def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    grid_shape = input_grid.shape

    # Find the red object(s)
    red_objects = find_objects(input_grid, 2)
    if not red_objects:  # Handle cases where no red object is present
        return output_grid
    red_object = red_objects[0] # Based on the example we will assume that there is only one object
    
    # Find white object
    white_objects = find_objects(input_grid, 0)
    if not white_objects:   # if no white object, return
        return output_grid

    # Find enclosed white areas within the red object and fill them with blue
    for white_obj in white_objects:
        if is_enclosed(white_obj, red_object, grid_shape):
            for r, c in zip(white_obj[0], white_obj[1]):
                output_grid[r, c] = 1

    return output_grid
```
