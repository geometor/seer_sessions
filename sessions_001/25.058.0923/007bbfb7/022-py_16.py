"""
The input 3x3 grid is used as a tile to construct a larger 9x9 output grid. The input grid is replicated nine times in a 3x3 arrangement, effectively tiling the output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a 9x9 array filled with zeros (white).
    output_grid = np.zeros((9, 9), dtype=int)

    # Get the dimensions of the input grid.
    input_height, input_width = input_grid.shape

    # Tile the input grid to create the output grid
    for i in range(3):
        for j in range(3):
            # Calculate the starting row and column indices for placing the input grid tile.
            row_start = i * input_height
            col_start = j * input_width

            # Place the input grid tile into the output grid.
            output_grid[row_start:row_start + input_height, col_start:col_start + input_width] = input_grid

    return output_grid