"""
1.  **Identify the Largest Blue Object:** In the input grid, locate the largest contiguous "object" composed of blue (1) pixels. Contiguous means pixels are connected horizontally or vertically (not diagonally).
2.  **Create a 3x3 Output Grid:** Create an output grid that is always 3x3, filled with black (0) pixels initially.
3. **Place Result:** Place a single blue pixel (1) at the center of the created 3x3 grid (row 1, column 1).
"""

import numpy as np

def transform(input_grid):
    # initialize 3x3 output grid with all zeros (black)
    output_grid = np.zeros((3, 3), dtype=int)

    # place a single blue pixel (1) at the center (row 1, column 1)
    output_grid[1, 1] = 1

    return output_grid