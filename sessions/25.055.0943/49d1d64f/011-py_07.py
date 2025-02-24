"""
The transformation rule takes an input grid and adds a border of black (0) pixels 
around it. The border is one pixel thick on all sides (top, bottom, left, and right).
"""

import numpy as np

def transform(input_grid):
    # Create a new, larger grid filled with black (0) pixels.
    input_height, input_width = input_grid.shape
    output_height = input_height + 2
    output_width = input_width + 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Copy the input grid into the center of the output grid.
    output_grid[1:output_height-1, 1:output_width-1] = input_grid

    return output_grid