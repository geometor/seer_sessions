"""
1.  **Identify Gray Pixels:** Locate all pixels in the input grid that have the value 5 (gray).
2.  **Third Column Transformation:** For all gray pixels, if the pixel is in the third column, change its value to 1 (blue).
3. **Seventh Column Transformation:** Check the seventh column from left. If a pixel in the column is gray (5) change it to red (2).
4.  **Preserve Other Pixels:** All other pixels retain their original values. The output grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    output_grid = np.copy(input_grid)  # Initialize output_grid as a copy of input_grid

    rows = len(input_grid)
    cols = len(input_grid[0]) if rows > 0 else 0

    # Iterate through each cell of the input grid
    for i in range(rows):
        for j in range(cols):
            # Third Column Transformation: Change gray(5) to blue(1)
            if j == 2 and input_grid[i][j] == 5:
                output_grid[i][j] = 1
            # Seventh Column Transformation:  change Gray(5) to Red(2)
            elif j == 6 and input_grid[i][j] == 5:
                output_grid[i][j] = 2

    return output_grid