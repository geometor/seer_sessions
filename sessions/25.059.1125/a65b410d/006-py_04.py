"""
1.  **Identify** all pixels with the value '2' (red) in the input grid.
2.  **For each** red pixel:
    *   Create a green '3' pixel in the cell directly above the red pixel, if the cell exists within the grid boundaries. Continue creating green '3' pixels upwards in a straight vertical line until the top edge of the grid is reached.
3.  **Find** the left-most red '2' pixel. Create one blue pixel ('1') one row directly below it.
4. **Retain** all original red '2' pixels in their original positions.
5.  All other pixels that were '0' (white) in the input grid remain '0' (white).
"""

import numpy as np

def get_red_pixels(grid):
    # Find coordinates of all red pixels (value 2).
    red_pixels = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r,c] == 2:
                red_pixels.append((r,c))
    return red_pixels

def transform(input_grid):
    output_grid = np.copy(input_grid)
    red_pixels = get_red_pixels(input_grid)

    if not red_pixels:
        return input_grid # handles the case where there are no red pixels.

    for r, c in red_pixels:
      # grow green upwards
      for i in range(r -1, -1, -1):
        output_grid[i,c] = 3

    # grow blue downwards
    leftmost_red_x = min(red_pixels, key=lambda item: item[1])[0]
    leftmost_red_y = min(red_pixels, key=lambda item: item[1])[1]

    if leftmost_red_x + 1 < output_grid.shape[0]:
       output_grid[leftmost_red_x + 1, leftmost_red_y] = 1
    
    return output_grid