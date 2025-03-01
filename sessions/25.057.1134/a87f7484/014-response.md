# a87f7484 • 014 • example_3 • investigate_coder

---
```python
"""
The transformation extracts a 3x3 subgrid from the input grid. This subgrid is defined by the arrangement of yellow (color code 4) pixels.  The output grid contains only yellow and white pixels, representing the configuration of the yellow pixels within their bounding area.
"""

import numpy as np

def find_object_by_color(grid, color):
    """Finds the coordinates of all pixels of a specified color."""
    coords = np.argwhere(grid == color)
    return coords

def get_bounding_box(coords):
    """Calculates the bounding box of a set of coordinates."""
    min_y, min_x = np.min(coords, axis=0)
    max_y, max_x = np.max(coords, axis=0)
    return min_y, min_x, max_y, max_x

def extract_subgrid(grid, bounding_box):
  """Extracts subgrid defined by the bounding box"""
  min_y, min_x, max_y, max_x = bounding_box
  return grid[min_y:max_y+1, min_x:max_x+1]


def transform(input_grid):
    """Extracts a subgrid based on yellow pixels in the input"""
    # Find all yellow pixels
    yellow_coords = find_object_by_color(input_grid, 4)

    # Determine the bounding box formed by the yellow pixels.
    bounding_box = get_bounding_box(yellow_coords)
    min_y, min_x, max_y, max_x = bounding_box
    
    height = max_y - min_y + 1
    width = max_x - min_x + 1
        
    if height != 3 or width != 3:
      yellow_coords_extended = []
      for y_offset in range(3):
          for x_offset in range(3):
            found = False
            for yc in yellow_coords:
               if (yc[0] - min_y, yc[1]-min_x) == (y_offset, x_offset):
                  found = True
                  break
            if not found:
              yellow_coords_extended.append([min_y+y_offset,min_x+ x_offset] )
      for new_coord in yellow_coords_extended:
           yellow_coords = np.vstack([yellow_coords, new_coord])
      bounding_box = get_bounding_box(yellow_coords)


    # Extract the region
    output_grid = extract_subgrid(input_grid, bounding_box)

    return output_grid
```
