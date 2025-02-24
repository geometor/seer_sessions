"""
The output grid is a 1x1 grid. The value of the single cell in the output grid is determined by the presence of any non-zero pixels in the input grid. If any non-zero pixels are present in the input grid, the output cell's value is 1. If there are no non-zero pixels (all pixels are 0), the output cell's value is 0.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Initialize the output grid as a 1x1 NumPy array with a default value of 0.
    output_grid = np.zeros((1, 1), dtype=int)

    # Check for the presence of any non-zero pixels in the input grid.
    if np.any(input_array != 0):
        # If any non-zero pixels are found, set the output cell's value to 1.
        output_grid[0, 0] = 1
    else:
        # If all pixels are 0, the output cell remains 0 (default value).
        output_grid[0, 0] = 0

    return output_grid.tolist()