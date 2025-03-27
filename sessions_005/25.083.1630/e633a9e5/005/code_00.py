"""
The transformation rule involves expanding the input grid into an output grid where each dimension (rows and columns) is twice the size of the corresponding input dimension. Each element in the input grid is duplicated to create a 2x2 block of the same value in the output grid. This effectively tiles the input grid both horizontally and vertically, doubling its size in each direction.
"""

import numpy as np

def transform(input_grid):
    # Get the dimensions of the input grid.
    input_rows, input_cols = input_grid.shape

    # Calculate the dimensions of the output grid.
    output_rows = input_rows * 2
    output_cols = input_cols * 2

    # Initialize the output grid with zeros.
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate through the input grid and duplicate each element.
    for i in range(input_rows):
        for j in range(input_cols):
            # Create a 2x2 block in the output grid.
            output_grid[2*i, 2*j] = input_grid[i, j]
            output_grid[2*i + 1, 2*j] = input_grid[i, j]
            output_grid[2*i, 2*j + 1] = input_grid[i, j]
            output_grid[2*i + 1, 2*j + 1] = input_grid[i, j]

    return output_grid