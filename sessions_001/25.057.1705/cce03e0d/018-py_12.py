"""
The output size is determined as follows: If the input grid has a dimension of 1 and any corresponding output grid dimension is 30, the output dimensions will be 30x30. The input is replicated to fill the output dimensions. Otherwise, the output dimensions are double the input dimensions, and the input grid is replicated twice in each dimension.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape

    # Determine output dimensions
    if (input_height == 1 or input_width == 1) and (any(dim == 30 for dim in [input_height * 30, input_width * 30 if input_height==1 else input_width * 1])):
          output_height, output_width = 30, 30
    else:
        output_height, output_width = input_height * 2, input_width * 2

    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Calculate scaling factors
    vertical_scaling_factor = output_height // input_height if input_height > 0 else 1
    horizontal_scaling_factor = output_width // input_width if input_width > 0 else 1

    # Replicate and tile the input grid
    for i in range(vertical_scaling_factor):
        for j in range(horizontal_scaling_factor):
            output_grid[i*input_height:(i+1)*input_height, j*input_width:(j+1)*input_width] = input_grid

    return output_grid.tolist()