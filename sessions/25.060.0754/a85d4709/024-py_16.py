"""
The transformation rule can be described as follows:

1.  **Grid Structure:** The input is a 3x3 grid of pixels, and the output maintains the same 3x3 structure.

2.  **Pixel-wise Transformation:** For each pixel in the input grid:

    *   If the pixel's color is gray (5), change it to green (3) in the output grid.
    *   If the pixel's color is white (0), change it to yellow (4) in the output grid.
    *   If the pixel color is blue(1), it remains blue (1).
    *   Otherwise, the pixel's color remains the same.

3.  **Output:** The result is a 3x3 output grid where the pixel colors have been transformed according to the rules above.

In essence, the program performs a color substitution on a pixel-by-pixel basis, preserving the grid's dimensions. Gray pixels become green, white pixels become yellow, and other colors are preserved.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same dimensions as the input.
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel of the input grid.
    for i in range(rows):
        for j in range(cols):
            # Apply the transformation rules based on the input pixel's value.
            if input_grid[i, j] == 5:  # If gray
                output_grid[i, j] = 3  # Change to green
            elif input_grid[i, j] == 0:  # If white
                output_grid[i, j] = 4  # Change to yellow
            else:
                output_grid[i,j] = input_grid[i,j] # transfer others

    return output_grid