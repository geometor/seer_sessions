"""
Iterate through each row of the input grid. For each row, check if all pixels have the same color.
If true, change the corresponding row in the output grid to all gray (5).
Otherwise, change the corresponding row in the output grid to all white (0).
"""

import numpy as np

def is_homogeneous(row):
    # Check if all elements in the row are the same
    return np.all(row == row[0])

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid to get the same dimensions
    output_grid = np.zeros_like(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0]) if rows > 0 else 0
    # Iterate through each row of the input grid
    for i in range(rows):
        # Check if the current row is homogeneous
        if is_homogeneous(input_grid[i]):
            # If homogeneous, set the corresponding row in output_grid to 5 (gray)
            output_grid[i, :] = 5
        else:
            # if not homogeneous, it remains all zeros (default initialization value)
            pass
    return output_grid