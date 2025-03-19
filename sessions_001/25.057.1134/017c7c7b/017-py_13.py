"""
The input grid is extended by mirroring each column, including the center column, outwards.  
The output grid's dimensions are calculated as follows:
- Output width: 2 * (input width) - 1
- Output height: 2 * (input height) - 1
The center column of the input is also the center column of the output.
"""

import numpy as np

def transform(input_grid):
    # Get input dimensions
    input_height, input_width = input_grid.shape

    # Calculate output dimensions
    output_height = 2 * input_height - 1
    output_width = 2 * input_width - 1

    # Initialize output grid with zeros
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Fill the output grid
    for i in range(input_width):
        # Copy the input column to the output
        output_grid[0:input_height, i] = input_grid[:, i]
        # Mirror the column to the right side
        output_grid[0:input_height, output_width - 1 - i] = input_grid[:, i]

    #Complete mirroring on rows
    for j in range(output_width):
        output_grid[input_height:output_height, j] = output_grid[0:input_height-1, j][::-1] #mirror the sub-array

    return output_grid