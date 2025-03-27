"""
1.  **Input:** A grid of any size containing pixel values representing colors.
2.  **Output:** Create a 3x3 output grid.
3.  **Transformation Rule:**
    *   Identify all pixels with color maroon (9) in the *input* grid.
    *   For each maroon pixel found, set the pixel at the same x,y coordinate in the output grid to color red (2).
    *   Set all other pixels in the output grid to white (0), regardless of color in the input.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a 3x3 array filled with white (0)
    output_grid = np.zeros((3, 3), dtype=int)

    # Iterate through the top 3x3 region of the input grid
    for i in range(min(3, input_grid.shape[0])):  # Ensure we don't go out of bounds
        for j in range(min(3, input_grid.shape[1])): # Ensure we don't go out of bounds
            # Map maroon (9) to red (2)
            if input_grid[i, j] == 9:
                output_grid[i, j] = 2
            # All other input pixels map to white (0) - this is implicitly handled
            # by initializing the output_grid to all zeros.

    return output_grid