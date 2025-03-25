"""
1.  **Identify Red Pixels:** Find the coordinates of all red pixels (value '2') in the input grid.

2.  **Find Leftmost and Rightmost Red per Row:** For each row in the grid, determine the coordinates of the leftmost and rightmost red pixels, if any red pixels exist in that row.

3.  **Fill Between Reds:** For each row, if leftmost and rightmost red pixels were found, iterate through the columns between those two pixels (inclusive). Change any white pixel (value '0') within this range to yellow (value '4').

4.  **Copy Other Pixels:** Copy all pixels (including red and other colors) that *were not* changed in step 3 directly to the output grid. This includes all pixels in rows without any red pixels and the pixels outside the left-right boundaries.
"""

import numpy as np

def get_red_pixels(grid):
    """Finds coordinates of all red pixels."""
    return np.argwhere(grid == 2)

def find_leftmost_rightmost_red_per_row(grid, red_pixels):
    """Finds the leftmost and rightmost red pixel in each row."""
    rows = grid.shape[0]
    leftmost_rightmost = {}  # Store as {row_index: (leftmost_col, rightmost_col)}
    for r in range(rows):
        leftmost_rightmost[r] = (None, None)

    for r, c in red_pixels:
        if leftmost_rightmost[r][0] is None or c < leftmost_rightmost[r][0]:
            leftmost_rightmost[r] = (c, leftmost_rightmost[r][1])
        if leftmost_rightmost[r][1] is None or c > leftmost_rightmost[r][1]:
            leftmost_rightmost[r] = (leftmost_rightmost[r][0], c)
    return leftmost_rightmost
    

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid.
    output_grid = np.copy(input_grid)
    rows, _ = input_grid.shape

    # Get coordinates of all red pixels.
    red_pixels = get_red_pixels(input_grid)

    # Find the leftmost and rightmost red pixel for each row
    leftmost_rightmost_reds = find_leftmost_rightmost_red_per_row(input_grid, red_pixels)

    # Iterate through each row
    for r in range(rows):
      left, right = leftmost_rightmost_reds[r]
      # Fill between leftmost and right most pixels
      if left is not None and right is not None:
        for c in range(left + 1, right):
          if output_grid[r,c] == 0:
            output_grid[r, c] = 4

    return output_grid