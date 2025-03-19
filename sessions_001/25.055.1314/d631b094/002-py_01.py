"""
1. Identify Blue Pixels: Examine the input grid and identify all pixels with a value of 1 (representing the color blue).
2. Count Blue Pixels: Count the total number of blue pixels found in the input grid.
3. Create Output Grid: Construct a new grid. Its width equals the count from Step 2, and height is one. Fill all cells in this new grid with blue pixel (value 1).
"""

import numpy as np

def transform(input_grid):
    # Count blue pixels (value 1)
    blue_pixel_count = np.count_nonzero(input_grid == 1)

    # Create output grid: 1 row, width equal to the blue pixel count, filled with 1s.
    output_grid = np.ones((1, blue_pixel_count), dtype=int)

    return output_grid