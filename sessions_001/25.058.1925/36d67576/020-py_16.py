"""
1.  **Identify Objects:** Examine the input grid.  An "object" is defined as *all* pixels of a given color, regardless of their spatial contiguity.

2.  **Focus on Yellow Objects:** Isolate the pixels that are yellow (color value 4).

3.  **Apply Transformation Based on Count:**
    *   If the number of yellow pixels is exactly 1, change that single pixel to green (color value 3).
    *   If the number of yellow pixels is greater than 1, change all yellow pixels to blue (color value 1).

4.  **Output Grid:** The final output is a new grid where the yellow pixels have been transformed according to the rules above, and all other pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""

    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find all yellow pixel coordinates
    yellow_pixels = np.argwhere(input_grid == 4)

    # Apply transformation based on the number of yellow pixels
    if len(yellow_pixels) == 1:
        # Single yellow pixel: change to green
        output_grid[yellow_pixels[0][0], yellow_pixels[0][1]] = 3
    elif len(yellow_pixels) > 1:
        # Multiple yellow pixels: change all to blue
        for row, col in yellow_pixels:
            output_grid[row, col] = 1

    return output_grid