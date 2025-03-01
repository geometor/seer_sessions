"""
The input grid is duplicated horizontally. The output grid's width is twice the input grid's width, while the height remains the same. The content of the input grid is copied, and the copy is placed directly to the right of the original.
"""

import numpy as np

def transform(input_grid):
    # Create a copy of the input grid.
    input_grid_copy = np.copy(input_grid)

    # Concatenate the original grid with its copy horizontally.
    output_grid = np.concatenate((input_grid, input_grid_copy), axis=1)

    return output_grid