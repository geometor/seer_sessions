"""
Transforms the input grid to a 1xN grid containing red pixels. The width (N) of the output grid 
corresponds to the number of rows in the input grid that contain at least one red pixel.
The output grid is always filled with red pixels.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the presence of red pixels in its rows.
    """
    input_array = np.array(input_grid)
    rows_with_red = np.any(input_array == 2, axis=1)  # Check for red pixels in each row
    num_rows_with_red = np.sum(rows_with_red)  # Count the rows containing red

    output_grid = np.full((1, num_rows_with_red), 2)  # Create output grid filled with red (2)

    return output_grid.tolist()