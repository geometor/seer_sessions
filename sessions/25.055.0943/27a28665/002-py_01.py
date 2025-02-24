"""
Counts the number of gray (5) pixels in the input grid. If the count is greater
than zero, then return blue (1).
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Count the number of gray pixels (5).
    gray_count = np.sum(input_array == 5)

    # Initialize output based on presence of gray
    if gray_count > 0:
      output_grid = [[1]]
    else:
      output_grid = [[0]] # default if not found - will need to be refined

    return output_grid