"""
The transformation rule identifies the rows and columns containing azure (8)
pixels in the input grid.  It then creates an output grid where the height is
the number of rows with azure pixels, and the width is the number of columns
with azure pixels. The output grid is filled entirely with azure (8) pixels.
"""

import numpy as np

def count_rows_with_azure(grid):
    # Count rows containing at least one azure (8) pixel.
    rows_with_azure = 0
    for row in grid:
        if 8 in row:
            rows_with_azure += 1
    return rows_with_azure

def count_cols_with_azure(grid):
    # Count columns containing at least one azure (8) pixel.
    cols_with_azure = 0
    for col in grid.T:  # Transpose to iterate through columns
        if 8 in col:
            cols_with_azure += 1
    return cols_with_azure
    

def transform(input_grid):
    # Count rows and columns with azure pixels.
    output_height = count_rows_with_azure(input_grid)
    output_width = count_cols_with_azure(input_grid)

    # Create an output grid filled with azure (8) pixels.
    output_grid = np.full((output_height, output_width), 8, dtype=int)

    return output_grid