"""
The output grid is created by copying rows from the top of the input grid. The number of rows copied is equal to `input_rows // 2`.
"""

import numpy as np

def transform(input_grid):
    """Transforms an input grid by taking the top n rows of it, where n is input_rows // 2."""
    # Get the dimensions of the input grid.
    rows, cols = input_grid.shape

    # Calculate the number of rows in the output grid (input rows // 2).
    output_rows = rows // 2

    # Initialize the output grid with the correct dimensions.
    output_grid = np.empty((output_rows, cols), dtype=int)

    # Copy the top n rows of the input grid to the output grid.
    output_grid = input_grid[:output_rows, :]
    
    return output_grid