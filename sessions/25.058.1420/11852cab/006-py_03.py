"""
Copy all pixels from row index 1 (the second row) to row index 5 (the sixth row).
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Iterate through the pixels of the second row (index 1).
    for x in range(output_grid.shape[1]):
        # Copy the pixel's value to the corresponding position in the sixth row (index 5).
        output_grid[5, x] = output_grid[1, x]

    return output_grid