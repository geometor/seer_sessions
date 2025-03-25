"""
The transformation rule involves expanding the input grid and overlaying a mirrored and padded version of the input onto a larger canvas. The padding appears to use the color azure (8). There's a definite sense of symmetry and mirroring in the output. Rows are added, and potentially stretched, with a reflection plane potentially lying in the middle of the rows and columns of the input.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_rows = len(input_grid)
    input_cols = len(input_grid[0])
    output_rows = (input_rows * 2) + 2
    output_cols = (input_cols * 2) + 2
    output_grid = np.full((output_rows, output_cols), 8, dtype=int)  # Initialize with azure (8)

    # change output pixels
    for i in range(input_rows):
        for j in range(input_cols):
            # Original position
            output_grid[i + 2, j + 2] = input_grid[i][j]

            # Mirror horizontally
            output_grid[i + 2, output_cols - 3 - j] = input_grid[i][j]
    
    for i in range(input_rows):
      for j in range(output_cols-4):
            # Mirror vertically
            output_grid[output_rows - 3 - i, j+2] = output_grid[i+2,j+2]

    return output_grid