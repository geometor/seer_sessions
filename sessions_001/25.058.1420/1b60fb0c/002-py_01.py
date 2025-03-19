"""
1.  **Identify the blue shape:** Locate the contiguous block of blue (1) pixels within the input grid.
2.  **Analyze the shape:** Determine the leftmost columns of the blue shape.
3. **Change to red**: Transform the leftmost columns to red(2) in all rows where it is found.
4.  **Output:** Return the modified grid, where the identified pixels within the blue shape have been changed to red, and all other pixels remain the same.
"""

import numpy as np

def find_blue_shape(grid):
    # Find all blue pixels
    blue_pixels = np.argwhere(grid == 1)
    return blue_pixels

def get_leftmost_columns(blue_pixels):
    # if there are no blue pixels, return an empty list
    if len(blue_pixels) == 0:
      return []

    # blue pixels is an array of [row, col]
    # we want unique columns
    columns = np.unique(blue_pixels[:, 1])
    
    #Find min column
    min_col = np.min(columns)

    return min_col

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find the blue shape
    blue_pixels = find_blue_shape(output_grid)

    # Get leftmost columns
    leftmost_col = get_leftmost_columns(blue_pixels)
    
    #Change leftmost column of blue shape to red.
    for row, col in blue_pixels:
      if col == leftmost_col:
        output_grid[row,col] = 2
      

    return output_grid