"""
The transformation rule is a direct copy. The output grid is identical to the input grid in terms of dimensions and pixel values. No changes are made to the input.
"""

import numpy as np

def transform(input_grid):
    """
    Copies the input grid to the output grid without any modifications.
    """
    # The output grid is the same as the input grid.
    output_grid = input_grid.copy()
    return output_grid