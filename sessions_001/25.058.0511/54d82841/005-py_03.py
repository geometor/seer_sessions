"""
1.  **Identify the bottom row:** Focus on the last row of the input grid.
2.  **Locate Black Pixels:** Within the bottom row, find pixels with the color black (value 0).
3. **Change to Yellow:** Change those specific black pixels to yellow (value 4).
4.  **Preserve Other Pixels:** All other pixels in the grid (those not in the bottom row, and those in the bottom row that are not black) remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = input_grid.copy()
    rows = output_grid.shape[0]
    cols = output_grid.shape[1]
    # Iterate through the bottom row
    for col in range(cols):
      #check if the pixel in the bottom row is black
      if output_grid[rows-1, col] == 0:
        #change the color to yellow
        output_grid[rows-1, col] = 4

    return output_grid