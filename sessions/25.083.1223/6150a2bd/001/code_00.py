"""
The transformation rule is a reflection across the main diagonal (top-left to bottom-right) followed by reversing the order of the rows.
1. Transpose: Treat the input grid as a matrix and transpose it. This means swapping rows and columns (element at `[i][j]` goes to `[j][i]`).
2. Reverse Rows: Reverse the order of rows in the transposed matrix. That it, the top row becomes the bottom row, the second row becomes the second-to-last row, and so on.
"""

import numpy as np

def transform(input_grid):
    # Transpose the input grid
    transposed_grid = np.transpose(input_grid)

    # Reverse the order of rows
    output_grid = np.flipud(transposed_grid)

    return output_grid.tolist()