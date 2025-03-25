"""
Iterate through each pixel in the input grid.

1.  Identify Target: Focus on pixels with a value *not* equal to black (0).
2.  Check Adjacent Pixel: Check the pixel immediately to the right.
3.  Black Pixel Condition: If the adjacent pixel is black (0), proceed to the next step.
4.  Lookahead Condition: Check the pixel two positions to the right of the *original* pixel (one position to the right of the black pixel).
5.  Color Copying: If the "lookahead" pixel has the same value as the pixel two positions to the left (the original pixel), change the color of the adjacent black pixel (the one immediately to the right of the original pixel) to the color of the original pixel. Otherwise do not modify pixels.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for r in range(rows):
        for c in range(cols):
            # Identify Target: Focus on non-black pixels.
            if input_grid[r, c] != 0:
                # Check Adjacent Pixel: Check pixel to the right.
                if c + 1 < cols and input_grid[r, c+1] == 0:
                    # Black Pixel Condition: Adjacent pixel is black.
                    # Lookahead Condition: Check two positions to the right.
                    if c + 2 < cols:
                        # Color Copying: Check if lookahead pixel matches original.
                        if input_grid[r, c+2] == input_grid[r, c]:
                            output_grid[r, c+1] = input_grid[r, c]

    return output_grid