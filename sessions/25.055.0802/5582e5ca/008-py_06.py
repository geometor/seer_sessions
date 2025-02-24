"""
The transformation rule is to replace all the pixels in the input grid with the color maroon (digit 9). Essentially, every cell value in the input grid, regardless of its initial value, is changed to 9 in the output grid. The dimensions of the grid remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input_grid to maintain dimensions
    output_grid = np.copy(input_grid)

    # change all output pixels to 9
    output_grid[:] = 9

    return output_grid