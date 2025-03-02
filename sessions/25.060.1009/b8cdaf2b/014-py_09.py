"""
1.  **Copy Bottom Rows:** Copy the bottom two rows of the input grid directly to the output grid. Preserve all pixel values and their positions.
2.  **Preserve other cells:** All other cells remain with their original value from the Input.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    h, w = output_grid.shape

    return output_grid