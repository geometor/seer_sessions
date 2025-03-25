"""
The transformation rule is as follows:
1. Iterate through the input grid, row by row, from top to bottom and left to right.
2. Maintain a color sequence counter, initialized to 1 (blue).
3. For each pixel:
    * If the pixel is gray (5):
        * Replace the pixel value with the current color from the sequence (1: blue, 2: red, 3: green).
        * Increment the color sequence counter, cycling back to 1 after 3.
    * If the pixel is not gray (5):
        *  Keep original Value (0, white).
4. Output the final grid.
"""

import numpy as np

def transform(input_grid):
    """Transforms an input grid according to the specified rule."""

    output_grid = np.copy(input_grid)
    color_sequence = [1, 3, 2]  # Blue, Green, Red
    color_index = 0

    for row_index, row in enumerate(input_grid):
        for col_index, pixel in enumerate(row):
            if pixel == 5:
                # Replace gray with the next color in the sequence
                output_grid[row_index, col_index] = color_sequence[color_index]
                color_index = (color_index + 1) % len(color_sequence)  # Cycle through colors
            # else no change

    return output_grid