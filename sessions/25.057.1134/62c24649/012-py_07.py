"""
The output grid dimensions are the sum of the input grid dimensions. The input grid is replicated to all four corners of the larger output grid, resulting in complete overlap.
"""

import numpy as np

def transform(input_grid):
    # Get input grid dimensions
    input_rows, input_cols = input_grid.shape

    # Determine output grid dimensions (sum of input dimensions)
    output_rows = input_rows + input_rows
    output_cols = input_cols + input_cols

    # Initialize output grid with zeros
    output_grid = np.full((output_rows, output_cols), input_grid[0,0])

    return output_grid