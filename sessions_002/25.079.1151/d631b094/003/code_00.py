"""
1.  **Identify:** Scan the input grid to find the single non-zero digit.
2.  **Count Pixels:** Count the number of pixels with the non-zero color.
3. **Create Output Grid:** create a 1 x N grid, where N is the number of non-zero pixels.
4.  **Fill:** Fill the output grid with the identified non-zero digit.
"""

import numpy as np

def transform(input_grid):
    # Convert input to numpy array
    input_array = np.array(input_grid)

    # Find the non-zero digit
    non_zero_digit = input_array[input_array != 0][0]

    # Count non-zero pixels
    pixel_count = np.sum(input_array == non_zero_digit)

    # Create output grid
    output_grid = np.full((1, pixel_count), non_zero_digit)

    return output_grid.tolist()