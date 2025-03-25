"""
Transforms an input grid into an output grid by expanding it in a 3x3 block-like fashion with a checkerboard pattern, using the top-left pixel of the input grid as the background color.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the described expansion and checkerboard rule.
    """
    input_grid = np.array(input_grid)
    background_color = input_grid[0, 0]
    output_height = (input_grid.shape[0] * 3) - 2
    output_width = (input_grid.shape[1] * 3) - 2
    output_grid = np.full((output_height, output_width), background_color, dtype=int)

    # Iterate through the input grid and place values into the output grid.
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            output_grid[i * 2, j * 2] = input_grid[i, j]

    return output_grid.tolist()