"""
The transformation rule involves identifying the element in the upper-right corner of the input grid and using that element to fill an entirely new output grid of the same dimensions.
"""

import numpy as np

def transform(input_grid):
    # Create output_grid with same dimensions as input, filled with zeros.
    output_grid = np.zeros_like(input_grid)

    # Identify the element in the upper-right corner.
    target_element = input_grid[0, -1]

    # Fill the output_grid with the target element.
    output_grid[:] = target_element

    return output_grid