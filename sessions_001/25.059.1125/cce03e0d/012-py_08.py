"""
The input grid is replicated three times within a larger output grid. The output grid's dimensions are three times the input grid's dimensions. The replicas are placed at the top-right, bottom-left, and bottom-right corners of the output grid. The rest of the output grid is filled with zeros.
"""

import numpy as np

def transform(input_grid):
    # Determine the dimensions of the input grid.
    input_height, input_width = input_grid.shape

    # Calculate the dimensions of the output grid (3 times the input).
    output_height = input_height * 3
    output_width = input_width * 3

    # Initialize the output grid with zeros.
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Place the first copy (top-right corner).
    output_grid[0:input_height, (output_width - input_width):output_width] = input_grid

    # Place the second copy (bottom-left corner).
    output_grid[(output_height - input_height):output_height, 0:input_width] = input_grid

    # Place the third copy (bottom-right corner).
    output_grid[(output_height - input_height):output_height, (output_width - input_width):output_width] = input_grid

    return output_grid