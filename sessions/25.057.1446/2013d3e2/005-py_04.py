"""
1.  **Identify:** Find all objects in the input grid. An object is a contiguous block of non-zero pixels.
2.  **Copy:**  Copy each object from the input grid to the output grid, maintaining its original color, shape, and position. If a cell in the input grid is 0, the corresponding cell in the output is also zero.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid.  This automatically
    # handles the case where 0 pixels remain 0, and copies the values and shape
    output_grid = np.copy(input_grid)

    # Since output_grid is initialized as a copy of input_grid, no further
    # operations are necessary.  The copy operation inherently handles the
    # object identification and copying with the correct position and color.

    return output_grid