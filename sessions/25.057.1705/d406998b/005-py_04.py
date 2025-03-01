"""
The transformation rule is an identity transformation. The output grid is an exact copy of the input grid. Every pixel's color and position remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Copies the input grid to the output grid (identity transformation).
    """
    # The output grid is a direct copy of the input grid.
    output_grid = np.copy(input_grid)
    return output_grid