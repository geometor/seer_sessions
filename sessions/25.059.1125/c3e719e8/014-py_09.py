"""
The input grid is replicated four times in a 2x2 pattern. The output grid's dimensions are three times the input grid's dimensions. The four copies of the input grid are placed within the output grid in a 2x2 arrangement.
"""

import numpy as np

def transform(input_grid):
    # Determine Output Size: The output grid's dimensions are three times the input grid's dimensions.
    input_height, input_width = input_grid.shape
    output_height = input_height * 3
    output_width = input_width * 3

    # Create Output Grid: Initialize an output grid filled with zeros.
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Place Replicas: Position the four copies within the output grid in a 2x2 arrangement.
    # Top-Left
    output_grid[:input_height, :input_width] = input_grid
    # Top-Right
    output_grid[:input_height, input_width * 2:input_width * 3] = input_grid
    # Bottom-Left
    output_grid[input_height * 2:input_height * 3, :input_width] = input_grid
    # Bottom-Right
    output_grid[input_height * 2:input_height * 3, input_width * 2:input_width * 3] = input_grid

    return output_grid