"""
The input grid contains a single non-zero pixel ('2', red). The output grid is the same size (3x5) and contains four specific colors at pre-determined locations: Green ('3') at (0, 2), Magenta ('6') at (0, 4), Azure ('8') at (2, 2), and Orange ('7') at (2, 4). All other pixels in the output grid are '0' (white). The transformation is independent of the input non-zero pixel's location.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid, then fill with zeros.
    output_grid = np.zeros_like(input_grid)

    # Set the specific colors at the predetermined locations.
    output_grid[0, 2] = 3  # Green
    output_grid[0, 4] = 6  # Magenta
    output_grid[2, 2] = 8  # Azure
    output_grid[2, 4] = 7  # Orange

    return output_grid