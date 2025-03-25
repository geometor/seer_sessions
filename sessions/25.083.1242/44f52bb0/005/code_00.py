"""
Counts the number of red pixels (value 2) in the input grid.
If the count is 2, 3, or 4, the output is 7.
If the count is 5 or 6, the output is 1.
"""

import numpy as np

def count_red_pixels(grid):
    """Counts the number of red pixels (value 2) in the grid."""
    return np.sum(grid == 2)

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""

    # Count the number of red pixels.
    red_count = count_red_pixels(input_grid)

    # Determine the output based on the red pixel count.
    if 2 <= red_count <= 4:
        output = 7
    elif 5 <= red_count <= 6:
        output = 1
    else:
        output = 1 # Added a default to return, though this should not be reachable with the known inputs.

    return output