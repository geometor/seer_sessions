"""
The input grid is replicated/expanded by a factor of 2. Then a 1 pixel border of color `0` is placed around it.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule:
    1.  Each pixel in the input grid is expanded into a 2x2 block in the output grid.
    2.  The expanded grid is surrounded by a border of '0' (white) pixels.
    """
    input_height, input_width = input_grid.shape
    output_height = input_height * 2 + 2
    output_width = input_width * 2 + 2

    # initialize output_grid with all zeros (white)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through the input grid and replicate each pixel
    for row in range(input_height):
        for col in range(input_width):
            color = input_grid[row, col]
            # Calculate the top-left corner of the 2x2 block in the output grid
            output_row = 2 * row + 1
            output_col = 2 * col + 1
            # Fill the 2x2 block with the input pixel's color
            output_grid[output_row:output_row+2, output_col:output_col+2] = color

    return output_grid