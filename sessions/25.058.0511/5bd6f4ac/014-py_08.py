"""
1.  **Focus on Row:** Identify the third row within the input grid.
2.  **Filter Colors:** Within that third row, disregard any white color (represented by 0).
3.  **Construct Output:** Create a 3x3 output grid. Populate it with the non-white colored from the third row of the input grid, from left to right. Maintain the relative ordering of the colors as they appear in the input row, and preserve the color values (numbers).
4. **All other values**: are 0 (white)
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Get the third row of the input grid.
    third_row = input_grid[2, :]

    # Filter out the white pixels (value 0).
    non_white_pixels = third_row[third_row != 0]

    # Ensure we don't exceed the output grid size.
    num_pixels_to_copy = min(len(non_white_pixels), 9)

    # Populate the output grid.
    row,col = 0, 0
    for i in range(num_pixels_to_copy):
      output_grid[row,col] = non_white_pixels[i]
      col += 1
      if col > 2:
        col = 0
        row += 1

    return output_grid