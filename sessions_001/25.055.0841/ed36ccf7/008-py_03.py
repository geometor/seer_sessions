"""
1. Rotate: The input grid is rotated 90 degrees clockwise.
2. Preserve Magenta: All magenta (6) pixels remain in their new rotated positions.
3. No Change: All other pixels and colors remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a rotated version of input_grid.
    output_grid = np.rot90(input_grid, k=-1)

    # All pixels, including magenta, are already in their correct positions
    # after rotation. No further changes are needed.

    return output_grid