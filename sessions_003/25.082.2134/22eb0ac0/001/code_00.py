"""
Iterates through each row of the input grid.
If a row contains exactly two non-zero pixels, and these pixels have the same color,
the entire row in the output grid is filled with that color.
Otherwise, the row remains unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the rule described above.
    """
    output_grid = np.copy(input_grid)  # Initialize output as a copy of the input
    rows, cols = input_grid.shape

    for i in range(rows):
        # Find non-zero pixels in the current row
        non_zero_pixels = []
        for j in range(cols):
            if input_grid[i, j] != 0:
                non_zero_pixels.append((j, input_grid[i, j]))  # (column, color)

        # Check if there are exactly two non-zero pixels with the same color
        if len(non_zero_pixels) == 2 and non_zero_pixels[0][1] == non_zero_pixels[1][1]:
            # Replicate the color across the entire row
            color = non_zero_pixels[0][1]
            output_grid[i, :] = color

    return output_grid