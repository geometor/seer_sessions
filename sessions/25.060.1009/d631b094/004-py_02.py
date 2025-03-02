"""
1.  **Identify and Count:** Examine the input grid and count the number of blue pixels (value 1).
2.  **Create Output Grid:** Create a new grid. The dimensions are 1 x *N*, where *N* is the count of blue pixels from step 1.
3. **Populate:** Fill every cell of the output grid with a blue pixel (value 1).
"""

import numpy as np

def count_blue_pixels(grid):
    # Count the number of blue pixels (value 1) in the grid.
    return np.count_nonzero(grid == 1)

def transform(input_grid):
    # Count the number of blue pixels in the input grid.
    blue_count = count_blue_pixels(input_grid)

    # Create a new grid with dimensions 1 x blue_count, filled with blue pixels (value 1).
    output_grid = np.ones((1, blue_count), dtype=int)

    return output_grid