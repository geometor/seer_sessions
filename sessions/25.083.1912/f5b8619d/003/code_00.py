"""
The transformation rule expands the input grid into a larger output grid with dimensions double those of the input.
Non-zero pixels in the input become 2x2 blocks of the same color in the output.
Zeros in the input grid become 8s (azure) in the output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with dimensions (input_height * 2, input_width * 2)
    input_height, input_width = input_grid.shape
    output_grid = np.zeros((input_height * 2, input_width * 2), dtype=int)

    # Iterate through the input grid
    for row in range(input_height):
        for col in range(input_width):
            # If the input pixel is non-zero, create a 2x2 block in the output grid
            if input_grid[row, col] != 0:
                output_grid[row*2:row*2+2, col*2:col*2+2] = input_grid[row, col]

    # Fill the output grid
    for row in range(output_grid.shape[0]):
        for col in range(output_grid.shape[1]):
           if output_grid[row, col] == 0:
               output_grid[row,col] = 8
    
    return output_grid