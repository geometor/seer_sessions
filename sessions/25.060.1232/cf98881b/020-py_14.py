"""
1.  **Identify Input:** Obtain the input grid.
2.  **Find Gray Pixels:** Locate all pixels with the color gray (value 5).
3.  **Change Color to White:** Change the color of these pixels to White (value 0).
4.  **Output:** output the modified grid
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find all pixels with the color gray (value 5)
    gray_pixels = np.where(output_grid == 5)

    # Change the color of these pixels to white (value 0)
    output_grid[gray_pixels] = 0

    return output_grid