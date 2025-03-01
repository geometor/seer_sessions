"""
Iterate through each pixel of the input grid. If a pixel is gray (5), 
and its horizontal position/index in the row is greater or equal to 5, and divisible by 3,
replace it with green (3). Otherwise, keep the original color.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    output_grid = np.copy(input_grid)  # Initialize output grid as a copy
    rows, cols = output_grid.shape

    # Iterate through each pixel
    for r in range(rows):
        for c in range(cols):
            # Check if the pixel is gray (5)
            if output_grid[r, c] == 5:
                # Check if the column index meets replacement criteria.
                if c >= 5 and c % 3 == 0:
                    output_grid[r, c] = 3  # Replace with green (3)

    return output_grid