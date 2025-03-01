"""
The input grid can be of any size. The output grid is always 3x3. The center column of the output grid (index 1) always contains red (2).  The remaining cells of the output grid are always white (0). The bottom-right pixels of the input grid are not relevant.
"""

import numpy as np

def transform(input_grid):
    # Initialize a 3x3 output grid with all zeros (white).
    output_grid = np.zeros((3, 3), dtype=int)

    # Set the entire center column to red (2).
    output_grid[:, 1] = 2

    return output_grid