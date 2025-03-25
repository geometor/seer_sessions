"""
Iterate through each pixel of the input grid.
Identify pixels that are red (color value 2).
For each red pixel, check if its row index is greater than or equal to half the total number of rows (rows // 2).
Also check if the sum of the row index and column index is odd.
If both conditions (bottom half AND odd sum of indices) are true, change the pixel's color to azure (color value 8).
Output the modified grid.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the rule described above."""
    
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)  # Initialize output grid

    for i in range(rows):
        for j in range(cols):
            # Check if the pixel is red (2)
            if input_grid[i, j] == 2:
                # Check if the pixel is in the bottom half and if the sum of row and col indices is odd
                if i >= rows // 2 and (i + j) % 2 != 0:
                    output_grid[i, j] = 8  # Replace with azure (8)
    
    return output_grid