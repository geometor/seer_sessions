"""
Iterate through each row of the input grid.
Count the number of white (0) pixels in the current row.
Create the output grid with 3x3, and place that number in the output grid.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid to the output grid by counting white pixels in each row and encoding."""

    # Get the number of rows in the input grid
    num_rows = len(input_grid)
    output_grid = []

    # Iterate through each row of the input grid
    for row in input_grid:
        # Count the number of white (0) pixels in the current row
        white_pixel_count = np.count_nonzero(row == 0)
        output_grid.append([white_pixel_count, white_pixel_count, white_pixel_count])
    
    return output_grid