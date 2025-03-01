"""
The input grid is embedded into a larger output grid. The output grid's dimensions are determined by multiplying the input grid's dimensions: the output width is twice the input width plus one, and the output height is three times the input height. The input grid is placed at the top-left corner of the second 'band' of rows, and the rest of the grid is filled with white (0).
"""

import numpy as np

def transform(input_grid):
    # Get input dimensions
    input_height, input_width = input_grid.shape

    # Calculate output dimensions
    output_height = input_height * 3
    output_width = input_width * 2 + 1

    # Create an output grid filled with white (0).
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Calculate the starting row index for embedding.
    start_row = input_height
    start_col = 0

    # Embed the input grid into the output grid.
    output_grid[start_row:start_row + input_height, start_col:start_col + input_width] = input_grid

    return output_grid