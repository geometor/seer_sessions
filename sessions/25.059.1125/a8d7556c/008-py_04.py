"""
1.  **Identify Gray Pixels:** Find all pixels in the input grid that have the color gray (value 5).
2.  **Change Pixel Color:** Change the color of each identified gray pixel to red (value 2).
3.  **Output:** The output grid is the same as the input grid, except all gray pixels have been replaced with red pixels.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing all gray pixels with red pixels.
    """
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Iterate through all pixels and change gray pixels to red
    for row in range(output_grid.shape[0]):
        for col in range(output_grid.shape[1]):
            if output_grid[row, col] == 5:
                output_grid[row, col] = 2

    return output_grid