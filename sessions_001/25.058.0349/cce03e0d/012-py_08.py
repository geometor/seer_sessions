"""
The input grid is replicated twice within a larger output grid. The output grid's dimensions are three times the input grid's dimensions. One copy of the input is placed at the top-right corner, and another at the bottom-left corner of the output grid. The rest of the output grid is filled with zeros (color 0).
"""

import numpy as np

def transform(input_grid):
    # Determine output grid dimensions: three times the input dimensions.
    input_height, input_width = input_grid.shape
    output_height = 3 * input_height
    output_width = 3 * input_width

    # Create output grid filled with zeros.
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Place the first copy of the input grid at the top-right corner.
    output_grid[0:input_height, output_width - input_width:output_width] = input_grid

    # Place the second copy of the input grid at the bottom-left corner.
    output_grid[output_height - input_height:output_height, 0:input_width] = input_grid

    return output_grid