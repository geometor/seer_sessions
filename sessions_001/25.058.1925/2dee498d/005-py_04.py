"""
The transformation compresses the input grid horizontally. Within each row, consecutive runs of identical-colored pixels are represented by a single pixel of that color in the output. The output grid's width is determined by the number of color changes in each row.

"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = []

    # Iterate through each row of the input grid
    for row in input_grid:
        new_row = []
        current_color = None  # Keep track of the current color

        # Iterate through each pixel in the row
        for pixel in row:
            # If the pixel is different from current color
            if pixel != current_color:
                new_row.append(pixel) #append to preserve and continue
                current_color = pixel #update current

        output_grid.append(new_row)

    return output_grid