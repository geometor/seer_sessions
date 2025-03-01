"""
For each row in the input grid, count the number of blue (1) pixels.  Create a 3x3 output grid. If a row in the input grid had blue pixels, place a red (2) pixel in the same row of the output grid. The x-coordinate of the red pixel is equal to the count of blue pixels in the corresponding input row.
"""

import numpy as np

def transform(input_grid):
    # Initialize a 3x3 output grid with all white (0) pixels.
    output_grid = np.zeros((3, 3), dtype=int)

    # Iterate through each row of the input grid.
    for i, row in enumerate(input_grid):
        # Count the number of blue (1) pixels in the current row.
        blue_count = np.count_nonzero(row == 1)

        # If the count of blue pixels is greater than 0, place a red (2) pixel
        # in the output grid at the corresponding row and x-coordinate = blue_count.
        if blue_count > 0:
          output_grid[i, blue_count-1] = 2 # array index starts at 0

    return output_grid