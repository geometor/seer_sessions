"""
The program always outputs a 2x2 grid filled with azure (color 8), regardless of the content of the input grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize a 2x2 numpy array filled with 8 (azure).
    output_grid = np.full((2, 2), 8)

    # Return the output grid as a list.
    return output_grid.tolist()