"""
The transformation rule is applied selectively based on the presence and arrangement of gray pixels:

1.  **Check for Gray Pixels:** Examine the input grid. If there are no gray pixels, the output grid is identical to the input grid (no transformation occurs).

2. **Selective Application** It seems that if the gray count is divisible by 3, every 3rd gray is changed to green starting from the right, row-wise.

3.  **Row-wise Transformation:** Within each row, locate the gray pixels. Starting from the rightmost gray pixel in each row, change every third gray pixel to green.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the presence and arrangement of gray pixels.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Check for Gray Pixels
    total_gray_pixels = np.sum(input_grid == 5)
    if total_gray_pixels == 0:
      return output_grid

    # Selective application based on divisibility by 3.
    if total_gray_pixels % 3 == 0:
        # Iterate through each row
        for row in range(rows):
            # Find gray pixels in the current row, from right
            gray_pixels = []
            for col in reversed(range(cols)):
              if output_grid[row, col] == 5:
                gray_pixels.append(col)

            # Change every third gray pixel to green
            count = 0
            for col in gray_pixels:
                count += 1
                if count == 1:
                    output_grid[row, col] = 3
                if count == 3:
                    count = 0 # reset

    return output_grid