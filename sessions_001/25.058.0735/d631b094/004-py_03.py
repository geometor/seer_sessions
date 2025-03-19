"""
1.  **Count Blue Pixels:** Count the number of blue pixels (value '1') in the input grid.

2.  **Handle Zero Blue Pixels:**
    *   If there are no blue pixels in the input, the output is a 1x1 grid containing a single black pixel (value '0').

3.  **Create Output Grid (Blue Pixels Present):**
    *   If blue pixels are present, create a 1 x N grid, where N is the count of blue pixels.

4.  **Fill Output Grid:**
    *   Fill all cells of the output grid created in step 3 with blue pixels (value '1').
"""

import numpy as np

def transform(input_grid):
    # Count the number of blue pixels (value '1') in the input grid.
    blue_count = np.count_nonzero(input_grid == 1)

    # Handle the case where there are no blue pixels.
    if blue_count == 0:
        output_grid = np.zeros((1, 1), dtype=int)  # 1x1 grid with a black pixel (0)
    else:
        # Create a 1 x N grid, where N is the count of blue pixels.
        output_grid = np.ones((1, blue_count), dtype=int)  # Filled with blue pixels (1)

    return output_grid