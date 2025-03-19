"""
The transformation rule can be summarized as follows:

1.  **Initial Scan:** Examine the entire input grid.
2.  **Color Substitution:**
    *   Replace all occurrences of color '5' (grey) with color '0' (white).
3.  **Copy:** Copy all other values directly to the output grid in the same position.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Replace all 5s with 0s.
    output_grid[output_grid == 5] = 0

    return output_grid