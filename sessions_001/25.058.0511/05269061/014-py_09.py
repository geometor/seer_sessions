"""
The transformation extracts the non-zero values (8, 3, and 4) from the input grid and replicates them in a specific alternating pattern to fill the output grid, maintaining the original dimensions. The pattern is '4 8 3', repeating across rows and columns.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing zeros with a repeating pattern of 4, 8, and 3.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Define the repeating pattern
    pattern = [4, 8, 3]

    # Fill the output grid with the repeating pattern
    for i in range(rows):
        for j in range(cols):
            output_grid[i, j] = pattern[(i + j) % len(pattern)]

    return output_grid.tolist()