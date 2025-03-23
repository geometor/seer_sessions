"""
The transformation rule is: Reverse the order of the rows in the input grid. Do *not* change any pixel values.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Reverse the order of rows.
    output_grid = np.flipud(output_grid)

    return output_grid