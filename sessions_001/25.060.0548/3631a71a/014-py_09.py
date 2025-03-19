"""
The transformation rule is a simple color substitution. Every pixel with the value 9 (maroon) in the input grid is changed to the value 2 (red) in the output grid. All other pixels, specifically those with the value 0 (white), remain unchanged. The dimensions of the grid stay constant.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.  This ensures the dimensions are the same.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel of the grid.
    for row in range(rows):
        for col in range(cols):
            # Check if the current pixel's value is 9 (maroon).
            if input_grid[row, col] == 9:
                # Replace the pixel's value with 2 (red).
                output_grid[row, col] = 2

    return output_grid