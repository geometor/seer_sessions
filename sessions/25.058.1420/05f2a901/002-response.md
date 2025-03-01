# 05f2a901 • 002 • example_3 • investigate_coder

---
```python
"""
The transformation rule is as follows:

1. Identify the contiguous red (2) object and the contiguous azure (8) object within the input grid.
2. Relative Reposition, keeping the azure object fixed: Move the red and azure objects, effectively swapping their y-location in input and output. The azure object's position appears to be the anchor, and the red object moves relative to it.

"""

import numpy as np

def find_object(grid, color):
    """
    Finds the coordinates of a contiguous object of a specified color.
    """
    coords = np.argwhere(grid == color)
    if len(coords) == 0:
        return None
    return coords

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # Find the red and azure objects
    red_coords = find_object(input_grid, 2)
    azure_coords = find_object(input_grid, 8)
    
    if red_coords is None or azure_coords is None:
        return input_grid

    # Determine bounding box for red
    min_red_row = np.min(red_coords[:, 0])
    max_red_row = np.max(red_coords[:, 0])
     # Determine bounding box for azure object
    min_azure_row = np.min(azure_coords[:,0])

    # calculate red object offset, relative to min row
    red_y_offset =  min_red_row

    # move red object
    for coord in red_coords:
      new_y = coord[0] - red_y_offset + min_azure_row
      if 0 <= new_y < output_grid.shape[0]:  # Check boundaries
          output_grid[new_y, coord[1]] = 2

    # keep the azure object in place
    for coord in azure_coords:
        output_grid[coord[0], coord[1]] = 8
   
    return output_grid
```
