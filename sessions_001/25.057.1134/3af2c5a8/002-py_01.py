"""
The input grid is expanded to double its height and width. Each azure (8) pixel in the input grid is expanded into a 2x2 block of azure pixels in the output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height = input_height * 2
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # change output pixels 
    for row in range(input_height):
        for col in range(input_width):
            if input_grid[row, col] == 8:
                # expand azure pixel to 2x2 block
                output_grid[row * 2, col * 2] = 8
                output_grid[row * 2 + 1, col * 2] = 8
                output_grid[row * 2, col * 2 + 1] = 8
                output_grid[row * 2 + 1, col * 2 + 1] = 8

    return output_grid