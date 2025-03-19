"""
The transformation rule is to replace the entire input grid with a grid of the same dimensions filled with the color 6 (magenta). The input can contain objects of varying colors, shapes, and sizes. The number, color, size, nor position of input objects affect the output.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same dimensions as the input grid.
    output_grid = np.empty_like(input_grid)

    # Fill the entire output grid with the color 6 (magenta).
    output_grid[:] = 6

    return output_grid