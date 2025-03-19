"""
The transformation rule is to crop the input grid to the width of the output grid, retaining the leftmost part.
"""

import numpy as np

def transform(input_grid):
    """
    Crops the input grid to a predetermined width (3 columns in this specific ARC problem).

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the cropped output grid.
    """
    # Determine the target width (fixed to length of axis 1)
    output_width = int(len(input_grid[0]) / 3)

    # Crop the input grid
    output_grid = input_grid[:, :output_width]

    return output_grid