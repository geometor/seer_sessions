```python
"""
The transformation rule involves extending each non-zero colored pixel in the input grid vertically downwards in the output grid. The output grid has the same width as the input grid, and the output grid's height is fixed at 10. For each column, iterate through the input grid. If a pixel in the input grid has a non-zero color, that pixel, and all pixels directly below it in the output grid (same column), are set to that color. Pixels in the output which do not have a non-zero value above them in the input are 0.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extending each non-zero pixel downwards to
    the bottom of the output grid. The output grid has dimensions 10 x width of input.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    input_grid = np.array(input_grid)
    cols_in = input_grid.shape[1]

    # Determine output dimensions (rows = 10, cols = same as input)
    rows_out = 10
    cols_out = cols_in

    # Initialize output_grid with zeros
    output_grid = np.zeros((rows_out, cols_out), dtype=int)


    # Iterate through each column
    for c in range(cols_in):
        # Iterate through each row of the *input* grid
        for r in range(input_grid.shape[0]):
            # If the current cell in the *input* is non-zero
            if input_grid[r, c] != 0:
                # Fill down the output grid from the current row
                for r_below in range(r, rows_out):
                    output_grid[r_below, c] = input_grid[r, c]

    return output_grid
```