"""
The input, consisting of a single row of pixels, is replicated within a square output grid. The output grid's dimensions are determined by the input row's length, creating a square. Each row in the output is a copy of the input.
"""

import numpy as np

def transform(input_grid):
    # Get the length of the input row.
    input_length = input_grid.shape[1]

    # Create an output grid of size NxN filled with zeros.
    output_size = input_length
    output_grid = np.zeros((output_size, output_size), dtype=int)
    
    # Replicate the input row for each row of the output grid.
    for i in range(output_size):
        output_grid[i,:] = input_grid[0]

    return output_grid