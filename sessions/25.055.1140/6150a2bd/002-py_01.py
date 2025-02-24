"""
The input grid is rotated 90 degrees counter-clockwise to produce the output grid.

1.  **Rotate**: rotate the entire input grid by 90 degrees in the counter-clockwise direction
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same dimensions as the input grid.
    input_grid = np.array(input_grid)
    output_grid = np.rot90(input_grid, k=-1)

    return output_grid.tolist()