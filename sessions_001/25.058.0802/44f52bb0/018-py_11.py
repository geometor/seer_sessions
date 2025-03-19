"""
Counts the number of yellow and red pixels in the input grid.
If the number of yellow pixels is greater than 0 and the number of red pixels is 0, the output is a 1x1 white (0) pixel.
Otherwise, the output is a 1x1 blue (1) pixel.
"""

import numpy as np

def count_pixels(grid, color_value):
    # Count the number of pixels of a specific color in the grid.
    return np.sum(grid == color_value)

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_grid = np.array(input_grid)

    # Count the number of yellow (4) pixels.
    yellow_count = count_pixels(input_grid, 4)

    # Count the number of red (2) pixels.
    red_count = count_pixels(input_grid, 2)

    # Determine the output based on the counts.
    if yellow_count > 0 and red_count == 0:
        output_grid = np.array([[0]])  # 1x1 white pixel
    else:
        output_grid = np.array([[1]])  # 1x1 blue pixel

    return output_grid