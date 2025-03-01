"""
The transformation rule takes a 3x3 input grid and expands it into a 6x6 output grid. Each pixel in the input grid is replicated as a 2x2 block in the output grid. The color of each input pixel is duplicated in the output grid at positions (2*i, 2*j), (2*i+1, 2*j), (2*i, 2*j+1), and (2*i+1, 2*j+1), where (i, j) are the coordinates of the pixel in the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 3x3 input grid into a 6x6 output grid by replicating each
    pixel as a 2x2 block.
    """
    # Initialize the 6x6 output grid with zeros.
    output_grid = np.zeros((6, 6), dtype=int)

    # Iterate through the input grid.
    for i in range(3):
        for j in range(3):
            # Get the color of the current pixel.
            color = input_grid[i, j]

            # Apply the 2x2 block replication.
            output_grid[2*i, 2*j] = color         # Top-left
            output_grid[2*i + 1, 2*j] = color     # Bottom-left
            output_grid[2*i, 2*j + 1] = color     # Top-right
            output_grid[2*i + 1, 2*j + 1] = color # Bottom-right

    return output_grid