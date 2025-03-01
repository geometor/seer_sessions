"""
1.  **Locate Red Pixel:** Find the coordinates of the single red (value '2') pixel in the input grid. There will always be exactly one.
2.  **Output:** Return a 1x1 grid.
3. **Output Value:** The value of that one output is orange (7).
"""

import numpy as np

def transform(input_grid):
    # Find the coordinates of the red pixel (value '2').
    # np.where returns a tuple of arrays, one for each dimension.
    # Since we expect only one red pixel, we take the first element of each array.
    red_pixel_coords = np.where(input_grid == 2)
    row = red_pixel_coords[0][0]
    col = red_pixel_coords[1][0]

    # Create a 1x1 output grid with the orange color (7)
    output_grid = np.array([[7]])

    return output_grid