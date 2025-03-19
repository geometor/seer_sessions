"""
The transformation takes sparse green pixels and uses them as seed points to construct an outlined spiral frame. 
The original green pixels serve as a guide of where the spiral will turn. The output grid is same size of input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by expanding green pixels into a clockwise spiral frame.
    """
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape
    green_pixels = []

    # 1. Identify Starting Points (green pixels)
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 3:
                green_pixels.append((r, c))

    # build complete perimeter of the spiral
    top, bottom, left, right = 0, rows - 1, 0, cols - 1

    # 2. Expand Green Area: Create the spiral frame
    while top <= bottom and left <= right:
        # go right
        for i in range(left, right + 1):
            output_grid[top, i] = 3
        top += 1

        # go down
        for i in range(top, bottom + 1):
            output_grid[i, right] = 3
        right -= 1

        if top <= bottom:
            # go left
            for i in range(right, left - 1, -1):
                output_grid[bottom, i] = 3
            bottom -= 1

        if left <= right:
            # go up
            for i in range(bottom, top - 1, -1):
                output_grid[i, left] = 3
            left += 1

    # 3. create the inner spiral guided by the position of green dots
    for r, c in green_pixels:
      output_grid[r,c] = 3

      # go down one and left one
      if r+1 < rows:
        output_grid[r+1,c] = 3
      if c-1 >= 0:
        output_grid[r+1, c-1] = 3

      # down one and right two
      if r+1 < rows and c+2 < cols:
        output_grid[r+2,c+2] = 3

      # up two and right one
      if r-2 >= 0 and c+1 < rows:
        output_grid[r-2, c+1] = 3

      # up one and left two
      if r - 1 >= 0 and c - 2 >= 0:
        output_grid[r-1,c-2] = 3

    return output_grid