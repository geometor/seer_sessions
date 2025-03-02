"""
1.  **Identify Blue Objects:** Find all contiguous regions of blue (1) pixels in the input grid.  Treat each contiguous block as a separate object.
2.  **Direct Transformation:**  For *every* blue pixel in the input grid, change the corresponding pixel in the output grid to red (2).  Do not rely on bounding boxes; perform a direct color swap based on the presence of blue.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with the same dimensions and all zeros,
    # then copy the input grid to preserve non-blue pixels.
    output_grid = np.copy(input_grid)

    # Iterate through all pixels in the input grid
    for row_index, row in enumerate(input_grid):
        for col_index, pixel_value in enumerate(row):
            # If a pixel is blue (1) in the input, change it to red (2) in the output
            if pixel_value == 1:
                output_grid[row_index, col_index] = 2

    return output_grid