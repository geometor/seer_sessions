"""
The input grid is replicated as a 2x2 tile to form the output grid.  The output grid's dimensions are exactly twice the height and twice the width of the input grid. Each pixel in the output grid corresponds to a pixel in the input grid, determined by finding the remainder of the output pixel's row and column indices divided by the input grid's height and width, respectively. The color/value of each pixel in the output is identical to its corresponding pixel in the input.
"""

import numpy as np

def transform(input_grid):
    # Determine Input Dimensions: Get the height and width of the input grid.
    input_height, input_width = input_grid.shape

    # Calculate Output Dimensions: Multiply both the height and width by two to get the output grid's dimensions.
    output_height, output_width = input_height * 2, input_width * 2

    # Create Output Grid: Initialize an empty output grid with the calculated dimensions.
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Replicate Input: Iterate through each cell of the *output* grid.
    for i in range(output_height):
        for j in range(output_width):
            # For each cell, calculate its corresponding position in the *input* grid
            # using the modulo operator (%) with the input grid's dimensions.
            input_row = i % input_height
            input_col = j % input_width

            # Copy the value from the corresponding input cell to the current output cell.
            output_grid[i, j] = input_grid[input_row, input_col]

    return output_grid