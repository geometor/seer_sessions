"""
Transformation Rule:
1. Identify: Locate all non-zero pixels within the input grid.
2. Extract: Record the color and original location of each non-zero pixel.
3. Clear: Make all of the input image zero
4. Rearrange: reposition the non-zero pixels to the bottom right of the grid, filling empty spaces from the left of the row to the right, and rows from the bottom row and up, preserving the color of the original cells.
5. Fill: Ensure any unassigned spaces is filled with white pixels (zeros).
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid by moving non-zero pixels to the bottom-right."""

    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)
    non_zero_pixels = []

    # 1. Identify and 2. Extract non-zero pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                non_zero_pixels.append((input_grid[r, c], (r, c)))

    # 3. Clear (already done during initialization)

    # 4. Rearrange: Position non-zero pixels to bottom-right
    pixel_index = 0
    for r in range(rows -1, -1, -1):      #start at bottom row
        for c in range(cols -1, -1, -1):  #start at rightmost col
            if pixel_index < len(non_zero_pixels):
                output_grid[r,c] = non_zero_pixels[pixel_index][0]
                pixel_index += 1

    # 5. Fill (already done during initialization)

    return output_grid.tolist()