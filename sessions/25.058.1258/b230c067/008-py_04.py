"""
1.  **Identify Target Pixels:** Iterate through each pixel in the input grid. The pixels of interest are those with the value 8 (azure).

2.  **Recolor Target Pixels:**
    a. If the azure pixel is in the top right corner area (defined, in this case, by rows 1-3 and colums 7-9 inclusive), change the color to 2 (red)
    b. If the azure pixel is not in that top right corner area, change the color of the azure pixel to 1 (blue).

3.  **Preserve Other Pixels:** All other pixels (those not azure) retain their original color/value.

4.  **Output:** The resulting grid, with recolored pixels, becomes the output.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""

    output_grid = np.copy(input_grid)  # Initialize output grid
    rows, cols = output_grid.shape

    # Iterate through each pixel
    for i in range(rows):
        for j in range(cols):
            # Recolor azure pixels based on location
            if output_grid[i, j] == 8:
                if 1 <= i <= 3 and 7 <= j <= 9:
                     output_grid[i,j] = 2
                else:
                    output_grid[i, j] = 1

    return output_grid