"""
The transformation rule is to create an output grid that is always 2 rows and 2 columns larger than the input grid and place the input at the very center.
"""

import numpy as np

def transform(input_grid):
    # Determine Input Dimensions
    input_rows, input_cols = input_grid.shape

    # Calculate Output Dimensions
    output_rows = input_rows + 2
    output_cols = input_cols + 2

    # Create Output Grid
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Center Calculation
    row_start = (output_rows - input_rows) // 2
    col_start = (output_cols - input_cols) // 2

    # Embed Input
    output_grid[row_start:row_start + input_rows, col_start:col_start + input_cols] = input_grid

    return output_grid