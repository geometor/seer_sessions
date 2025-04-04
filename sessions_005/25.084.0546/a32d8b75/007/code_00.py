"""
The transformation removes all white (0) and magenta (6) pixels. Remaining colored regions are stacked vertically in each column, maintaining their original relative vertical order.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by removing white (0) and magenta (6) pixels and stacking the
    remaining colored regions, maintaining relative vertical order within each column.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Iterate through each column
    for j in range(cols):
        # Collect non-white, non-magenta pixels in the column, preserving their original row order
        column_pixels = []
        for i in range(rows):
            pixel = input_grid[i, j]
            if pixel != 0 and pixel != 6:  # Filter out white and magenta
                column_pixels.append(pixel)

        # Place the collected pixels in the output column, starting from the top, maintaining original order
        for i, pixel in enumerate(column_pixels):
            output_grid[i, j] = pixel

    return output_grid.tolist()