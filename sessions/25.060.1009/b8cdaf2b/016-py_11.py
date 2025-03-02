"""
1.  **Copy Input:** The output grid is created by copying the input grid exactly. The shape and all pixel values remain identical.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid by cloning the input grid
    output_grid = np.copy(input_grid)

    # No changes needed as output_grid is already a perfect copy.

    return output_grid