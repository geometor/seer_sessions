"""
1.  **Identify:** Locate all non-zero pixels within the input grid.
2.  **Extract:** Record the color and original position (row, column) of each non-zero pixel, *in the order they appear from top-to-bottom and left-to-right within the input grid*.
3.  **Clear:** Create an output grid of the same dimensions as the input, filled entirely with zeros (white pixels).
4.  **Rearrange:** Iterate through the recorded non-zero pixels *in their original order*. Place each pixel in the output grid, starting from the bottom-right corner. Fill cells moving from right-to-left. Once a row is full, move to the row above, again filling from right-to-left.
5.  **Fill:** (Implicit) The output grid is initialized with zeros, so any remaining spaces will automatically be white.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid, preserving relative order of non-zero pixels."""

    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)
    non_zero_pixels = []

    # 1. Identify and 2. Extract non-zero pixels (top-to-bottom, left-to-right)
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                non_zero_pixels.append((input_grid[r, c], (r, c)))

    # 3. Clear (already done during initialization)

    # 4. Rearrange: Position non-zero pixels to bottom-right (preserving order)
    pixel_index = 0
    for r in range(rows - 1, -1, -1):  # Start at bottom row
        for c in range(cols - 1, -1, -1):  # Start at rightmost col
            if pixel_index < len(non_zero_pixels):
                output_grid[r, c] = non_zero_pixels[pixel_index][0]
                pixel_index += 1

    return output_grid.tolist()