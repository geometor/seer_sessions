"""
The transformation rule is a vertical flip, or a reflection of the grid across its horizontal axis.  For each cell at `input[i][j]`, the corresponding cell in the output grid is `output[rows - 1 - i][j]`, where `rows` is the number of rows in the grid. This operation is equivalent to flipping the input grid upside down. This works for both square and rectangular grids.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by vertically flipping it.
    """
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = [[0] * cols for _ in range(rows)]  # Initialize output grid with zeros

    for i in range(rows):
        for j in range(cols):
            output_grid[rows - 1 - i][j] = input_grid[i][j] # Perform the vertical flip

    return output_grid