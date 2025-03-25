"""
The transformation rule replicates each pixel in the input grid into a square block in the output grid. 
The dimensions of the square block are determined by the dimensions of the input grid. If the input grid is N x N, each pixel becomes an N x N block.
"""

import numpy as np

def transform(input_grid):
    # Get input grid dimensions
    input_height = len(input_grid)
    input_width = len(input_grid[0])

    # Calculate output grid dimensions based on replication factor (which is input_height)
    replication_factor = input_height
    output_height = input_height * replication_factor
    output_width = input_width * replication_factor

    # Initialize output grid with zeros
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through input grid and replicate elements
    for i in range(input_height):
        for j in range(input_width):
            # Get the current pixel value
            pixel_value = input_grid[i][j]

            # Calculate the starting row and column for the replicated block
            start_row = i * replication_factor
            start_col = j * replication_factor

            # Replicate the pixel value into the corresponding N x N block in the output grid
            for row in range(start_row, start_row + replication_factor):
                for col in range(start_col, start_col + replication_factor):
                    output_grid[row, col] = pixel_value

    return output_grid