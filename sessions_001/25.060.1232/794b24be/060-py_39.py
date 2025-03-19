"""
1.  **Copy Input:** Create a copy of the input grid to serve as the output grid.
2.  **Identify and Transform:** Iterate through each pixel of the *input* grid.  If a pixel is blue (color value 1), change the corresponding pixel in the *output* grid to red (color value 2).
3.  **Preserve Other Colors:** All pixels in the input grid that are *not* blue should remain unchanged in the output grid (this is handled implicitly by copying the input grid initially).
"""

import numpy as np

def transform(input_grid):
    # Copy the input grid to the output grid.
    output_grid = np.copy(input_grid)

    # Iterate through each pixel of the input grid.
    for row_index, row in enumerate(input_grid):
        for col_index, pixel_value in enumerate(row):
            # If a pixel is blue (1) in the input, change it to red (2) in the output.
            if pixel_value == 1:
                output_grid[row_index, col_index] = 2

    return output_grid