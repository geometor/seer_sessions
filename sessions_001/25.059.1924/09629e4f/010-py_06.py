"""
Iterate through each pixel of the input grid. If a pixel is gray (5), copy it directly to the output grid. If a pixel is not gray, create a 3x3 block in the output grid with the same color, centered at the input pixel's location.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the defined rule."""

    rows, cols = input_grid.shape
    output_grid = np.full((rows, cols), 5)  # Initialize with gray (5)

    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] != 5:
                # Create 3x3 block
                for x in range(max(0, i - 1), min(rows, i + 2)):
                    for y in range(max(0, j - 1), min(cols, j + 2)):
                        output_grid[x, y] = input_grid[i, j]
            #else: #gray (5), already initialized
            #    output_grid[i,j] = input_grid[i,j]

    return output_grid