"""
The transformation rule is a vertical flip (reflection across the horizontal midline). The output grid is created by reversing the order of rows in the input grid.  For each row index `i` in the input grid, the row at index `i` in the input becomes the row at index `height - 1 - i` in the output grid, where `height` is the number of rows in the input grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of input
    output_grid = np.copy(input_grid)

    # flip the grid vertically
    output_grid = np.flipud(output_grid)

    return output_grid