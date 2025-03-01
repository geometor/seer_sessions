"""
Transforms a 3x3 input grid to a 3x3 output grid. 
Each row in the output grid is either all gray (5) or all white (0).
A row is mapped to gray if all pixels in the corresponding input row have the same color.
Otherwise, the row is mapped to white.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the color uniformity of each row.
    """
    output_grid = np.zeros((3, 3), dtype=int)  # Initialize output grid with white (0)

    for i in range(3):  # Iterate through rows
        row = input_grid[i]
        if np.all(row == row[0]):  # Check if all elements in the row are the same
            output_grid[i] = 5  # Set output row to gray (5)
        # else: output_grid[i] remains 0 (white), which is the initial value.

    return output_grid