"""
The output is always a 4x4 grid filled with gray (5), regardless of the input grid's size.
"""

import numpy as np

def transform(input_grid, example_outputs):  # Add example_outputs argument
    # Initialize a 4x4 output grid filled with gray (5).
    output_grid = np.full((4, 4), 5, dtype=int)

    return output_grid.tolist()