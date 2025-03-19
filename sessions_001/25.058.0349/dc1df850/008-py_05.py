"""
1.  **Identify** all pixels in the input grid that are not black (color 0).
2.  **Check** for a red (color 2) pixel in the top row.
3.  **If Found:** Create a blue (color value 1) pixel to the left of this pixel.
4. **Check** if the colored pixels are the red (2) pixel.
5.  **If Found:** create a 3x3 square of blue (color 1) pixels. The red pixel will not be a the center. The red pixel becomes part of the blue square. Place the red pixel at the center of the top edge of the square.
6. **Retain** other colored pixels and black background pixels as same location.
"""

import numpy as np

def find_pixels(grid, color):
    """Finds coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color)

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    output_grid = input_grid.copy()
    height, width = input_grid.shape

    # Find all non-black pixels
    colored_pixels = find_pixels(input_grid, 2)

    for r, c in colored_pixels:
      if r == 0 and c-1 >= 0:
        output_grid[r,c-1] = 1


    #create 3x3 square for any other red pixel
    for r, c in colored_pixels:
        if r != 0: #skip red pixel in the top row
          for i in range(r , r + 3):
              for j in range(c - 1, c + 2):
                  if 0 <= i < height and 0 <= j < width:  # Boundary check
                      output_grid[i, j] = 1
          output_grid[r,c] = 2

    return output_grid