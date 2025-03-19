"""
1.  **Check for Orange:** Examine the input grid for the presence of any orange pixels (pixels with a value of 7).
2.  **Conditional Transformation:**
    *   If orange pixels are present, copy *only* the orange pixels to the output grid in their exact same positions. All other pixels in the output should be 0.
    *   If no orange pixels are present, the output grid is an exact copy of the input grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid as all zeros with the same shape as the input
    output_grid = np.zeros_like(input_grid)

    # Check for the presence of orange pixels
    orange_pixels = (input_grid == 7)

    # Conditional Transformation
    if np.any(orange_pixels):
        # If orange pixels are present, copy them to the output grid
        output_grid[orange_pixels] = 7
    else:
        # If no orange pixels, output is identical to input
        output_grid[:] = input_grid

    return output_grid