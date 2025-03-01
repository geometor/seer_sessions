"""
Locate the maroon (9) pixel in the input grid.
Retain the maroon (9) pixel in the same location in the output grid.
Add rows above the maroon pixel, where each row alternates between yellow (4) and white (0), 
starting and ending with yellow, and having as many rows to occupy the space above, leaving the rest as white pixels.
"""

import numpy as np

def find_pixel_location(grid, color_value):
    # Find the location of a pixel with a specific color value.
    for r_idx, row in enumerate(grid):
        for c_idx, pixel in enumerate(row):
            if pixel == color_value:
                return (c_idx, r_idx)
    return None

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid.
    output_grid = np.copy(input_grid)
    
    # Find the location of the maroon pixel (value 9).
    maroon_location = find_pixel_location(input_grid, 9)
   
    # Add alternating rows of yellow and white above the maroon pixel.
    if maroon_location:
      row_pattern = [4, 0] * 5  # the row has length 9, using 5 pairs
      row_pattern = row_pattern[:9]
      for i in range(maroon_location[1]):
        if (maroon_location[1] -1 - i) % 2 == 0: # even rows starting from maroon
          output_grid[i] =  row_pattern

    return output_grid