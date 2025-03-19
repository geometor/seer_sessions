"""
1. **Background Change:** Change all background (white/0) pixels in the input grid to green (3) pixels in the output grid.
2. **Copy azure object:** The azure object of three adjacent pixels in a horizontal line is maintained.
3. **Extend azure:** The initial azure shape is extended downward by two pixels, resulting in an L shape, or the inverse of an L, depending on perspective.
4.  **Remove Red Pixel:** The single red pixel in the input is not present, or it transforms to green matching the background.
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

    # Find azure (8) pixels
    azure_coords = find_object(input_grid, 8)

    # Copy azure pixels to output grid
    for coord in azure_coords:
        output_grid[coord[0], coord[1]] = 8

    # extend azure object down, if there are azure pixels
    if (len(azure_coords) > 0):
      min_row = np.min(azure_coords[:,0])
      max_row = np.max(azure_coords[:,0])
      min_col = np.min(azure_coords[:,1])
      max_col = np.max(azure_coords[:,1])

      if max_row+2 < output_grid.shape[0]:
        output_grid[max_row+1,max_col] = 8
        output_grid[max_row+2,max_col] = 8

    return output_grid