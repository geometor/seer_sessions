"""
The transformation rule involves a 2x2 expansion of the input 3x3 grid. Each pixel in the input grid corresponds to a 2x2 block of the same color in the output grid. The relative positions and patterns of the colors are maintained during this expansion.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a 6x6 array filled with zeros.
    output_grid = np.zeros((6, 6), dtype=int)

    # Iterate through each pixel of the input grid.
    for i in range(3):
        for j in range(3):
            # Get the color of the current input pixel.
            color = input_grid[i, j]

            # Create a 2x2 block in the output grid with the same color.
            output_grid[2*i:2*i+2, 2*j:2*j+2] = color

    return output_grid