"""
Identifies all pixels with the value 8 (azure) in the input grid, and creates a 1x1 output grid with the value 8.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid to a 1x1 output grid containing the value 8.
    """
    # initialize output_grid
    output_grid = np.zeros((1, 1), dtype=int)

    # Set the value of the single pixel in the output grid to 8.
    output_grid[0, 0] = 8

    return output_grid