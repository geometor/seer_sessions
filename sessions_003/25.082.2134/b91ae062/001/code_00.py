"""
The transformation rule involves replicating each element of the input grid both horizontally and vertically. 
The output grid's dimensions are the product of the input grid's height and width. 
Each pixel in the input is expanded into a (input_width x input_height) rectangle in the output.
"""

import numpy as np

def transform(input_grid):
    # Get input grid dimensions
    input_height = len(input_grid)
    input_width = len(input_grid[0])

    # Calculate output grid dimensions
    output_height = input_height * input_height
    output_width = input_width * input_width

    # Initialize output grid with zeros
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through input grid and replicate elements
    for i in range(input_height):
        for j in range(input_width):
            # Get the current pixel value
            pixel_value = input_grid[i][j]

            # Calculate the starting row and column for the replicated block
            start_row = i * input_height
            start_col = j * input_width

            # Replicate the pixel value into the corresponding block in the output grid
            for row in range(start_row, start_row + input_height):
                for col in range(start_col, start_col + input_width):
                    output_grid[row, col] = pixel_value

    return output_grid