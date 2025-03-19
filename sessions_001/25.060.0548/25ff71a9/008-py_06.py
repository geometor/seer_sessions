"""
The transformation rule is a vertical flip (reflection across the horizontal midline). The output grid is created by inverting the row order of the input grid. Specifically, the top row of the input becomes the bottom row of the output, the middle row stays the same, and the bottom row of the input becomes the top row of the output.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of input
    output_grid = np.copy(input_grid)

    # flip the grid vertically
    output_grid = np.flipud(output_grid)

    return output_grid