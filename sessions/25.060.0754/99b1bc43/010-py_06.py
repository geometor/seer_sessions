"""
Conceptually divide the input grid into non-overlapping 2x2 blocks. For each block,
if color '1' (blue) is present, the corresponding output cell is '3' (green);
otherwise, it's '0' (white).
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_rows = rows // 2
    output_cols = cols // 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    for i in range(output_rows):
        for j in range(output_cols):
            # Define the 2x2 block in the input grid
            block = input_grid[2*i:2*i+2, 2*j:2*j+2]
            # Check for the presence of '1' (blue) in the block
            if 1 in block:
                output_grid[i, j] = 3  # Set to '3' (green)
            else:
                output_grid[i, j] = 0  # Set to '0' (white)

    return output_grid.tolist()