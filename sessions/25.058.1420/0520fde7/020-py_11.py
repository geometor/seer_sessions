"""
1.  **Initialize:** Create a 3x3 output grid filled with white pixels (value 0).
2.  **Iterate:** For each row in the input grid:
    *   **Count:** Count the number of blue pixels (value 1) in the current row.
    *   **Place:** If the count of blue pixels is greater than 0, place a red pixel (value 2) in the output grid. The red pixel will be on the same row. The red pixel's column is determined by the number of blue pixels. Column index starts at 0. So if one blue pixel is found, the column index = 0. If two are found, column index = 1, if three are found, column index = 2.
3. If a row has zero blue pixels, that row in the output remains all white.
"""

import numpy as np

def transform(input_grid):
    # Initialize a 3x3 output grid with all white (0) pixels.
    output_grid = np.zeros((3, 3), dtype=int)

    # Iterate through each row of the input grid.
    for i, row in enumerate(input_grid):
        # Count the number of blue (1) pixels in the current row.
        blue_count = np.count_nonzero(row == 1)

        # If the count of blue pixels is greater than 0, place a red (2) pixel
        # in the output grid at the corresponding row and x-coordinate = blue_count - 1.
        if blue_count > 0:
            output_grid[i, blue_count - 1] = 2

    return output_grid