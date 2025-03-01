# d4f3cd78 • 010 • example_2 • investigate_coder

---
```python
"""
1.  **Identify** the existing gray (5) shape in the input grid.
2.  **Find** the horizontal center of the grid.
3.  **Draw** a vertical line of azure (8) pixels, starting from the top edge of the gray shape, extending upwards to the top edge of the grid, aligned with the horizontal center.
4.  **Identify** the top row of the grey object.
5.  **Fill** with azure(8) any gray(5) pixels inside the shape that are directly below any azure(8) pixels.
"""

import numpy as np

def find_object_by_color(grid, color):
    """Finds the coordinates of all pixels of a specific color."""
    coords = np.argwhere(grid == color)
    return coords

def find_top_row_of_object(object_coords):
     """Finds the minimum row index (top row) of an object's coordinates."""
     if len(object_coords) == 0:
         return None
     return np.min(object_coords[:, 0])

def find_horizontal_center(grid):
    """Finds the horizontal center of the grid."""
    return grid.shape[1] // 2

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # Find the existing gray (5) shape
    gray_coords = find_object_by_color(input_grid, 5)
    
    # Find the horizontal center of the grid
    center_x = find_horizontal_center(input_grid)
    
    # Find the top row of the gray shape
    top_row = find_top_row_of_object(gray_coords)
    
    if top_row is not None:
        # Draw the vertical azure line
        for y in range(top_row):
            output_grid[y, center_x] = 8

        # Fill gray pixels below azure with azure.
        for x in range(input_grid.shape[1]):
          for y in range(top_row, input_grid.shape[0]):
            if output_grid[y,x] == 5:
              if output_grid[top_row-1, x] == 8:
                for y_fill in range(top_row,input_grid.shape[0]):
                  if output_grid[y_fill,x] == 5:
                    output_grid[y_fill,x] = 8
                  else:
                    break # stop when we hit something other than 5

    return output_grid
```
