"""
The input grid is duplicated horizontally to create the output grid. The output grid has the same height as the input but twice the width.
"""

import numpy as np

def transform(input_grid):
    # Get input grid dimensions
    height, width = input_grid.shape

    # Create output grid with double the width
    output_grid = np.zeros((height, width * 2), dtype=int)

    # Copy input grid to the left half of the output grid
    output_grid[:, :width] = input_grid

    # Copy input grid to the right half of the output grid
    output_grid[:, width:] = input_grid

    return output_grid