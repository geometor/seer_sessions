"""
Creates a new grid of the same dimensions as the input grid. Fills the main diagonal (from top-left to bottom-right) of the new grid with the value 5. All other cells in the new grid are filled with the value 0. The original values do not matter.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with the same dimensions as the input
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = np.zeros((rows, cols), dtype=int)

    # Iterate through the grid and fill the diagonal with 5
    for i in range(min(rows, cols)):
        output_grid[i, i] = 5

    return output_grid