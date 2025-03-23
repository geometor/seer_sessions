"""
The transformation rule is to take the input grid and create a new grid that's
twice as large in both dimensions, by tiling the original input grid four times
in a 2x2 pattern.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by doubling its dimensions and tiling the
    original pattern in a 2x2 arrangement.
    """
    # Get input grid dimensions
    input_height, input_width = input_grid.shape

    # Double dimensions for the output grid
    output_height = input_height * 2
    output_width = input_width * 2

    # Initialize the output grid with zeros
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Tile the input grid into the output grid
    for i in range(2):
        for j in range(2):
            output_grid[i * input_height:(i + 1) * input_height,
                        j * input_width:(j + 1) * input_width] = input_grid

    return output_grid