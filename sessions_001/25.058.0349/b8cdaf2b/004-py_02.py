"""
Replace white pixels in the top row with the color of the last non-white pixel in the same column.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Iterate through each pixel in the top row
    for j in range(cols):
        # Check if the pixel is white
        if input_grid[0][j] == 0:
            # Search the column from bottom to top
            for i in range(rows - 1, -1, -1):
                # Find the last non-white pixel
                if input_grid[i][j] != 0:
                    output_grid[0][j] = input_grid[i][j]
                    break  # Stop searching after finding the replacement color

    return output_grid