# 2bcee788 • 026 • refine_coder

---
```python
"""
1. **Background:** Change all white (0) pixels in the input grid to green (3) in the output grid.
2. **Azure Object:** Identify the horizontal line of three adjacent azure (8) pixels.
3. **Azure Extension:** Extend the azure object by creating a vertical segment of two pixels, changing it to a 3x3 L-shape. The segment is added to the column of the azure pixel on the side *opposite* of the initial red pixel. If no red pixel, extend to the left (This last part is an inference we need to test). The extension forms an "L" shape or a mirrored "L" shape.
4. **Red Removal:** Remove the red (2) pixel.
"""

import numpy as np

def find_object(grid, color):
    # return coordinates of the object with specified color.
    coords = np.argwhere(grid == color)
    if len(coords) > 0:
        return coords
    else:
        return []

def transform(input_grid):
    # initialize output_grid
    output_grid = np.full(input_grid.shape, 3)  # Fill with green (3)

    # Find azure (8) and red (2) pixels
    azure_coords = find_object(input_grid, 8)
    red_coords = find_object(input_grid, 2)

    # Copy azure pixels to output grid
    for coord in azure_coords:
        output_grid[coord[0], coord[1]] = 8

    # extend azure object down, if there are azure pixels
    if (len(azure_coords) > 0):
      min_row = np.min(azure_coords[:,0])
      max_row = np.max(azure_coords[:,0])
      min_col = np.min(azure_coords[:,1])
      max_col = np.max(azure_coords[:,1])

      # Determine which side to extend based on red pixel presence and position
      if len(red_coords) > 0:
          red_col = red_coords[0][1]
          if red_col > max_col:  # Red is to the right
              extend_col = min_col
          else:  # Red is to the left
              extend_col = max_col
      else:  # No red pixel, extend to the left (as per observation)
        extend_col = min_col

      
      # extend, ensuring not to overflow boundaries
      if max_row+2 < output_grid.shape[0]:
        output_grid[max_row+1,extend_col] = 8
        output_grid[max_row+2,extend_col] = 8

    return output_grid
```
