"""
The input grid is expanded. Each non-zero pixel in the original image becomes a 2x2 block. In these blocks, original value is at top-left and 8 fills the remaining positions. Zero-value pixels remain zeros and also expand, maintaining their original value of 0.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows * 2, cols * 2), dtype=int)

    # change output pixels
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] != 0:
                # Create a 2x2 block with original value at top-left and 8 elsewhere
                output_grid[i*2, j*2] = input_grid[i, j]
                output_grid[i*2 + 1, j*2] = 8
                output_grid[i*2, j*2 + 1] = 8
                output_grid[i*2 + 1, j*2 + 1] = 8
            else:
                # Expand zero pixels while keeping them zeros.
                output_grid[i*2:i*2 +2, j*2:j*2+2] = 0


    return output_grid.tolist()