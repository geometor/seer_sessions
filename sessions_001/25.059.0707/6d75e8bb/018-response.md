# 6d75e8bb • 018 • refine_coder

---
```python
"""
The azure shape is modified by changing some of its azure pixels to red.
The change starts from the left edge of an indentation.
If an azure pixel has a white pixel on it's immediate left,
the recoloring to red will begin and proceed leftward. The recoloring stops when the left most azure
pixel of that extent is reached.
"""

import numpy as np

def find_azure_shape(grid):
    # Find the coordinates of all azure (8) pixels.
    azure_coords = np.argwhere(grid == 8)
    return azure_coords

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find the azure shape.
    azure_coords = find_azure_shape(output_grid)
    if len(azure_coords) == 0:
        return output_grid

    # Iterate through rows
    for r in range(output_grid.shape[0]):
      #check each azure pixel
      for c in range(output_grid.shape[1]):
        if output_grid[r,c] == 8:
          #if the pixel to the immediate left is white
          if c > 0 and output_grid[r, c-1] == 0:
            # start recoloring path
            temp_c = c
            # find the leftmost azure pixel in current extent
            while temp_c >= 0 and output_grid[r, temp_c] == 8:
              temp_c -= 1
            leftmost_azure_col_in_row = temp_c + 1

            # recolor azure pixel to red until the leftmost point
            temp_c = c
            while temp_c >= leftmost_azure_col_in_row:
              output_grid[r, temp_c] = 2
              temp_c -= 1

    return output_grid
```
