"""
The output grid always consists of the first four columns of the input grid. Any colored objects
within the input grid that fall completely or partially within the first four columns are
preserved in the output grid, in their original relative positions within those four columns.
If a colored object lies entirely outside the first four columns, it is not included in the output.

Another way to say this: The output is a cropped version of the input. The cropping window is
always from column 0 to column 3 (inclusive) and spans all rows.
"""

import numpy as np

def transform(input_grid):
    """
    Crops the input grid to the first four columns, preserving any colored objects within that region.
    """
    input_grid = np.array(input_grid)
    output_grid = input_grid[:, :4]  # Select the first four columns
    return output_grid.tolist()
