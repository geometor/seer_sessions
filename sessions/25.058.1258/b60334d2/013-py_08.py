"""
Creates a 9x9 output grid with a specific alternating pattern, regardless of the input grid's content. The pattern consists of alternating rows: one with alternating gray (5) and blue (1) pixels, and the other with alternating blue (1) and white (0) pixels.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same dimensions as the input (which will be 9x9)
    output_grid = np.zeros_like(input_grid)
    rows, cols = output_grid.shape

    # Fill the output grid row by row
    for i in range(rows):
        if i % 2 == 0:  # Even rows (0-indexed)
            for j in range(cols):
                output_grid[i, j] = 5 if j % 2 == 0 else 1
        else:  # Odd rows
            for j in range(cols):
                output_grid[i, j] = 1 if j % 2 == 0 else 0

    return output_grid