"""
1.  **Identify Target Pixels:** Iterate through each pixel in the input grid. The pixels of interest are those with the value 8 (azure).

2.  **Recolor Target Pixels:**
    a. If the azure pixel is in the first row where azure appears, change color to 2 (red).
    b. If the azure pixel is not in the first row where azure appears, change color to 1 (blue)

3.  **Preserve Other Pixels:** All other pixels (those not azure) retain their original color/value.

4.  **Output:** The resulting grid, with recolored pixels, becomes the output.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""

    output_grid = np.copy(input_grid)  # Initialize output grid
    rows, cols = output_grid.shape
    first_azure_row = -1

    # Find the first row with an azure pixel
    for i in range(rows):
        for j in range(cols):
            if output_grid[i, j] == 8:
                first_azure_row = i
                break  # only processes first row
        if first_azure_row != -1:
          break

    # Iterate through each pixel
    for i in range(rows):
        for j in range(cols):
            # Recolor azure pixels based on location
            if output_grid[i, j] == 8:
                if i == first_azure_row:
                     output_grid[i,j] = 2
                else:
                    output_grid[i, j] = 1

    return output_grid