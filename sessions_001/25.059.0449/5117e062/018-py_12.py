"""
Create a 3x3 output grid filled entirely with green (value 3), regardless of the input grid's content.
"""

import numpy as np

def transform(input_grid):
    # Initialize a 3x3 output grid filled with zeros.
    output_grid = np.zeros((3, 3), dtype=int)

    # Fill the entire output grid with the value 3 (green).
    output_grid[:] = 3

    return output_grid